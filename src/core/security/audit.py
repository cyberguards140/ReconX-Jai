import datetime
import logging
from typing import Any

logger = logging.getLogger(__name__)


class AuditLogger:
    """
    Secure append-only audit logging for compliance and security forensics.
    """

    @staticmethod
    def log_event(
        user_id: str, tenant_id: str, action: str, resource: str, metadata: dict[str, Any] = None
    ):
        """
        Records a security-relevant event.
        """
        # In production, this would write to a specialized WORM (Write Once Read Many) storage or SIEM.
        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "user_id": user_id,
            "tenant_id": tenant_id,
            "action": action,
            "resource": resource,
            "metadata": metadata or {},
        }

        logger.info(f"[AUDIT] {log_entry}")


audit_logger = AuditLogger()
