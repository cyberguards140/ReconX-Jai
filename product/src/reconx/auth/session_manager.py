import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from reconx.database.models import Session
from cachetools import TTLCache
import asyncio
from typing import Optional

# In-memory cache for fast session validation: max 10000 items, TTL 5 minutes
session_cache = TTLCache(maxsize=10000, ttl=300)

MAX_CONCURRENT_SESSIONS = 5
IDLE_TIMEOUT_MINUTES = 60

async def create_session(db: AsyncSession, user_id: str, tenant_id: Optional[str], ip_address: str, user_agent: str) -> Session:
    # Check concurrent sessions
    stmt = select(Session).where(
        Session.user_id == user_id, 
        Session.is_active == True
    ).order_by(Session.created_at.asc())
    
    result = await db.execute(stmt)
    active_sessions = result.scalars().all()
    
    # Revoke oldest if limit exceeded
    if len(active_sessions) >= MAX_CONCURRENT_SESSIONS:
        sessions_to_revoke = active_sessions[:len(active_sessions) - MAX_CONCURRENT_SESSIONS + 1]
        for s in sessions_to_revoke:
            s.is_active = False
            s.logout_time = datetime.now(timezone.utc)
            if s.session_id in session_cache:
                del session_cache[s.session_id]

    session_id = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=IDLE_TIMEOUT_MINUTES)
    
    new_session = Session(
        session_id=session_id,
        user_id=user_id,
        tenant_id=tenant_id,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=expires_at,
        is_active=True
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    session_cache[session_id] = True
    return new_session

async def validate_session(db: AsyncSession, session_id: str) -> bool:
    if session_cache.get(session_id) is True:
        return True
    
    stmt = select(Session).where(
        Session.session_id == session_id, 
        Session.is_active == True
    )
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    
    if not session:
        return False
        
    # Python timestamp comparisons requires aware datetime
    if session.expires_at:
        # DB expires_at might be naive depending on sqlite/postgres config, let's normalize
        exp = session.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp < datetime.now(timezone.utc):
            session.is_active = False
            await db.commit()
            return False
        
    session_cache[session_id] = True
    return True

async def update_last_seen(db: AsyncSession, session_id: str):
    stmt = select(Session).where(Session.session_id == session_id)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    if session:
        session.last_seen = datetime.now(timezone.utc)
        session.expires_at = datetime.now(timezone.utc) + timedelta(minutes=IDLE_TIMEOUT_MINUTES)
        await db.commit()

async def revoke_session(db: AsyncSession, session_id: str):
    stmt = select(Session).where(Session.session_id == session_id)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    if session:
        session.is_active = False
        session.logout_time = datetime.now(timezone.utc)
        await db.commit()
        if session_id in session_cache:
            del session_cache[session_id]

async def revoke_all_user_sessions(db: AsyncSession, user_id: str):
    stmt = select(Session).where(Session.user_id == user_id, Session.is_active == True)
    result = await db.execute(stmt)
    sessions = result.scalars().all()
    
    for s in sessions:
        s.is_active = False
        s.logout_time = datetime.now(timezone.utc)
        if s.session_id in session_cache:
            del session_cache[s.session_id]
            
    await db.commit()
