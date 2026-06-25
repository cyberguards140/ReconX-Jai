from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from data.database.models import AuditLog


async def log_security_event(
    db: AsyncSession,
    action: str,
    actor: str | None = None,
    user_id: str | None = None,
    tenant_id: str | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    resource: str | None = None,
    status: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    request_path: str | None = None,
    method: str | None = None,
    response_status: int | None = None,
    execution_time: float | None = None,
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
        timestamp=datetime.now(timezone.utc),
    )
    db.add(audit)
    await db.commit()
