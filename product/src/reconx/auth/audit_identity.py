from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from reconx.database.models import AuditLog
from typing import Optional

async def log_security_event(
    db: AsyncSession,
    action: str,
    actor: Optional[str] = None,
    user_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    resource: Optional[str] = None,
    status: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    request_path: Optional[str] = None,
    method: Optional[str] = None,
    response_status: Optional[int] = None,
    execution_time: Optional[float] = None
):
    """
    Logs an action to the audit_logs table with comprehensive identity and network context.
    """
    audit = AuditLog(
        actor=actor,
        user_id=user_id,
        tenant_id=tenant_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        resource=resource,
        status=status,
        ip_address=ip_address,
        user_agent=user_agent,
        request_path=request_path,
        method=method,
        response_status=response_status,
        execution_time=execution_time,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(audit)
    await db.commit()
