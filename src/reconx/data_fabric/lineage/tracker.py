import logging
from typing import Dict, Any, List
from datetime import datetime, timezone

from reconx.enterprise.isolation.tenant_context import get_current_tenant_id

logger = logging.getLogger(__name__)

class DataLineageTracker:
    """
    Tracks end-to-end provenance. (e.g., Raw Kafka Event -> Normalized Record -> Lakehouse)
    """
    def __init__(self):
        self._lineage_graph = []

    def record_transformation(self, source_id: str, target_id: str, operation: str):
        """
        Records that source_id was transformed into target_id via operation.
        """
        tenant_id = get_current_tenant_id() or "system"
        edge = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tenant_id": tenant_id,
            "source": source_id,
            "target": target_id,
            "operation": operation
        }
        self._lineage_graph.append(edge)
        logger.debug(f"Lineage tracked: {source_id} -> {operation} -> {target_id}")

    def get_lineage(self, target_id: str) -> List[Dict[str, Any]]:
        """Retrieves the history of a specific piece of data."""
        return [e for e in self._lineage_graph if e["target"] == target_id]

lineage_tracker = DataLineageTracker()
