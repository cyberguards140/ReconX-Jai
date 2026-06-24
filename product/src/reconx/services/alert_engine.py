from reconx.modules.automation.triggers import TriggerEngine

class AlertEngineService:
    @staticmethod
    def process_event(event_type: str, severity: str) -> dict:
        if TriggerEngine.should_trigger_alert(event_type, severity):
            return {"alert": True, "severity": severity, "message": f"Alert generated for {event_type}"}
        return {"alert": False}
