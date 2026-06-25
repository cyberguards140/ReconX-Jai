import logging
from datetime import datetime, timezone
from typing import Any

from reconx.enterprise.isolation.tenant_context import get_current_tenant_id

logger = logging.getLogger(__name__)


class GlobalSecurityTimeline:
    """
    Tracks chronological history across all domains (Decisions, Approvals, Detections, Simulations).
    Provides a unified audit trail and real-time operational ledger.
    """

    def __init__(self):
        # In-memory mock for the ledger. In production, this pulls directly from the Neo4j timeline/Postgres.
        self._timeline_events = []

    def log_event(self, event_type: str, source: str, payload: dict[str, Any]):
        """
        Appends a cross-domain event to the global timeline.
        """
        tenant_id = get_current_tenant_id() or "system"

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tenant_id": tenant_id,
            "type": event_type,
            "source": source,
            "payload": payload,
        }
        self._timeline_events.append(event)
        logger.debug(f"Timeline event recorded: {event_type} from {source}")

    def query_timeline(self, limit: int = 50) -> list[dict[str, Any]]:
        """
        Retrieves the most recent events for the current tenant.
        """
        tenant_id = get_current_tenant_id() or "system"
        # Filter for the tenant and return the most recent
        events = [e for e in self._timeline_events if e["tenant_id"] == tenant_id]
        return list(reversed(events))[-limit:]


global_timeline = GlobalSecurityTimeline()
