class IntegrationsCore:
    @staticmethod
    def format_slack_payload(message: str) -> dict:
        return {"text": message}
