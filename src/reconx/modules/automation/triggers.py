class TriggerEngine:
    @staticmethod
    def should_trigger_alert(event_type: str, severity: str) -> bool:
        return severity in ["Critical", "High"] and event_type == "NewFinding"
