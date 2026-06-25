import uuid
from datetime import datetime, timezone
from typing import Any

from reconx.modules.security_analytics.schema import NormalizedEventModel


class EventNormalizer:
    """
    Converts different event formats into a single, uniform schema.
    """

    def __init__(self):
        pass

    def normalize(self, raw_event: dict[str, Any]) -> NormalizedEventModel:
        return NormalizedEventModel(
            event_id=raw_event.get("id", f"evt_{uuid.uuid4().hex[:8]}"),
            timestamp=raw_event.get("timestamp", datetime.now(timezone.utc).isoformat()),
            event_type=raw_event.get("type", "unknown_event"),
            source=raw_event.get("source", "system"),
            asset_id=raw_event.get("asset_id", ""),
            severity=raw_event.get("severity", "low"),
            attributes=raw_event.get("attributes", {}),
        )
