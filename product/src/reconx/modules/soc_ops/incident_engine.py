import uuid
from reconx.modules.soc_ops.schema import IncidentModel
from typing import List, Dict, Any

class IncidentEngine:
    """
    Aggregates multiple correlated alerts and threat context into actionable Incidents.
    """
    def __init__(self):
        pass

    def correlate_into_incident(self, title: str, alerts: List[Dict[str, Any]]) -> IncidentModel:
        severity = "medium"
        for alert in alerts:
            if alert.get("severity") == "critical":
                severity = "critical"
                break
            elif alert.get("severity") == "high":
                severity = "high"
                
        return IncidentModel(
            incident_id=f"inc_{uuid.uuid4().hex[:8]}",
            title=title,
            severity=severity
        )
