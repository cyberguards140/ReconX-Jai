import uuid

from recon.modules.security_analytics.schema import AlertModel, NormalizedEventModel


class AlertEngine:
    """
    Manages the generation of actionable alerts.
    """

    def __init__(self):
        pass

    def generate_alert(self, score: int, event: NormalizedEventModel) -> AlertModel:
        severity = "low"
        if score > 80:
            severity = "critical"
        elif score > 60:
            severity = "high"
        elif score > 40:
            severity = "medium"

        return AlertModel(
            alert_id=f"alrt_{uuid.uuid4().hex[:8]}",
            severity=severity,
            title=f"Suspicious activity detected on {event.asset_id}",
            entities=[event.asset_id],
            evidence=[event.model_dump()],
        )
