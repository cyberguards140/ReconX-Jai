from typing import Dict, Any, List
from datetime import datetime, timezone
import uuid

class SnapshotEngine:
    """
    Tracks changes to infrastructure over time by taking historical snapshots.
    """
    def __init__(self):
        pass

    def take_snapshot(self, entities: List[Any], snapshot_type: str = "infrastructure") -> Dict[str, Any]:
        """
        Creates a snapshot of the current state of infrastructure entities.
        """
        snapshot_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc)
        
        snapshot_data = {
            "snapshot_id": snapshot_id,
            "snapshot_type": snapshot_type,
            "timestamp": timestamp.isoformat(),
            "entity_count": len(entities),
            "data": [entity.model_dump() for entity in entities]
        }
        
        return snapshot_data
