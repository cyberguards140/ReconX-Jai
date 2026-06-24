class WebhookService:
    @staticmethod
    def trigger(event_type: str, data: dict) -> dict:
        return {"event": event_type, "payload": data, "status": "sent"}
