from reconx.database.models import AuditLog
from reconx.database.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    pass


audit_log_repo = AuditLogRepository(AuditLog)
