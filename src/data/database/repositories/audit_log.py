from data.database.models import AuditLog
from data.database.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    pass


audit_log_repo = AuditLogRepository(AuditLog)
