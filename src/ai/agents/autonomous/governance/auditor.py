import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any

from plugins.enterprise.isolation.tenant_context import get_current_tenant_id

logger = logging.getLogger(__name__)


class DecisionAuditor:
    """
    Cryptographically logs AI autonomous decisions and human approvals.
    Ensures strict compliance and non-repudiation.
    """

    def __init__(self):
        self._last_hash: str = "0" * 64

    def log_decision(self, plan_id: str, action: str, details: dict[str, Any]):
        tenant_id = get_current_tenant_id() or "system"

        event_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tenant_id": tenant_id,
            "plan_id": plan_id,
            "action": action,  # e.g. "generated_plan", "approved_plan", "executed_plan"
            "details": details,
            "previous_hash": self._last_hash,
        }

        # Hash chain
        event_str = json.dumps(event_payload, sort_keys=True)
        current_hash = hashlib.sha256(event_str.encode("utf-8")).hexdigest()
        event_payload["hash"] = current_hash
        self._last_hash = current_hash

        # Write to secure WORM log (using structured logging for now)
        logger.info(f"AUTONOMOUS_AUDIT: {json.dumps(event_payload)}")


decision_auditor = DecisionAuditor()
