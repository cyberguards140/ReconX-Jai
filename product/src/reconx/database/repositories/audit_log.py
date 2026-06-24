from reconx.database.repositories.base import BaseRepository
from reconx.database.models import AuditLog


class AuditLogRepository(BaseRepository[AuditLog]):
    pass


audit_log_repo = AuditLogRepository(AuditLog)
