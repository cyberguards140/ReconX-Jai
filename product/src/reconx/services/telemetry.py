import json
from datetime import datetime

class TelemetryService:
    @staticmethod
    def log_event(service: str, event: str, metrics: dict = None) -> dict:
        payload = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "event": event,
            "metrics": metrics or {}
        }
        # In a real app this would write to stdout or a centralized logging platform
        return payload
