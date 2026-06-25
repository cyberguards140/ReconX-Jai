import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any

from plugins.enterprise.isolation.tenant_context import get_current_tenant_id

logger = logging.getLogger(__name__)


class AuditLogger:
    """
    Immutable, Cryptographically Chained Audit Logger.
    Creates a tamper-evident audit trail for all critical security and data actions.
    """

    def __init__(self):
        self._last_hash: str = "0" * 64
        # In a real implementation, this would write to a WORM (Write Once Read Many) storage
        # or forward directly to a secure Kafka topic `audit.events`
        self.kafka_producer = None  # Mocking for now

    def log_event(
        self,
        action: str,
        user_id: str,
        resource_type: str,
        resource_id: str,
        details: dict[str, Any] = None,
    ):
        """
        Logs a critical action (e.g., login, export, permission change).
        """
        tenant_id = get_current_tenant_id() or "system"
        timestamp = datetime.now(timezone.utc).isoformat()

        event_payload = {
            "timestamp": timestamp,
            "tenant_id": tenant_id,
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "previous_hash": self._last_hash,
        }

        # Create cryptographic chain
        event_str = json.dumps(event_payload, sort_keys=True)
        current_hash = hashlib.sha256(event_str.encode("utf-8")).hexdigest()
        event_payload["hash"] = current_hash

        # Update chain
        self._last_hash = current_hash

        # Write to secure log (stdout configured for JSON ingestion)
        logger.info(f"AUDIT_EVENT: {json.dumps(event_payload)}")

        # If Kafka was configured, send to `audit.events` topic
        if self.kafka_producer:
            # self.kafka_producer.publish("audit.events", event_payload)
            pass


audit_logger = AuditLogger()
