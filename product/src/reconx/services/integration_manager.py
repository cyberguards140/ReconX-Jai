from reconx.modules.enterprise.integrations import IntegrationsCore

class IntegrationManagerService:
    @staticmethod
    def prepare_slack_alert(msg: str) -> dict:
        return IntegrationsCore.format_slack_payload(msg)
