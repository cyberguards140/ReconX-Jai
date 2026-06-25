import logging
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any

from reconx.enterprise.isolation.tenant_context import get_current_tenant_id

logger = logging.getLogger(__name__)

class SimulationTracker:
    """
    Ensures that every theoretical scenario ran within the Decision Laboratory
    is logged, reproducible, and version controlled.
    """
    def __init__(self):
        self._last_hash: str = "0" * 64

    def log_simulation(self, scenario_type: str, theoretical_changes: Any, results: Dict[str, Any]):
        """
        Cryptographically records a simulation run.
        """
        tenant_id = get_current_tenant_id() or "system"
        
        event_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tenant_id": tenant_id,
            "scenario_type": scenario_type,
            "assumptions": theoretical_changes,
            "results": results,
            "previous_hash": self._last_hash
        }
        
        event_str = json.dumps(event_payload, sort_keys=True)
        current_hash = hashlib.sha256(event_str.encode('utf-8')).hexdigest()
        event_payload["hash"] = current_hash
        self._last_hash = current_hash
        
        logger.info(f"TWIN_SIMULATION_AUDIT: {json.dumps(event_payload)}")

simulation_tracker = SimulationTracker()
