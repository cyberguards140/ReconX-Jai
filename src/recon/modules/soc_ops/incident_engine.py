import uuid
from typing import Any

from recon.modules.soc_ops.schema import IncidentModel


class IncidentEngine:
    """
    Aggregates multiple correlated alerts and threat context into actionable Incidents.
    """

    def __init__(self):
        pass

    def correlate_into_incident(self, title: str, alerts: list[dict[str, Any]]) -> IncidentModel:
        severity = "medium"
        for alert in alerts:
            if alert.get("severity") == "critical":
                severity = "critical"
                break
            elif alert.get("severity") == "high":
                severity = "high"

        return IncidentModel(
            incident_id=f"inc_{uuid.uuid4().hex[:8]}", title=title, severity=severity
        )
