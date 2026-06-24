from reconx.database.repositories.base import BaseRepository
from reconx.database.models import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

class SessionRepository(BaseRepository[Session]):
    async def get_by_session_id(self, db: AsyncSession, session_id: str) -> Optional[Session]:
        res = await db.execute(select(Session).filter(Session.session_id == session_id))
        return res.scalars().first()

    async def get_active_sessions(self, db: AsyncSession, user_id: str) -> List[Session]:
        res = await db.execute(
            select(Session).filter(Session.user_id == user_id, Session.is_active.is_(True))
        )
        return list(res.scalars().all())


session_repo = SessionRepository(Session)
