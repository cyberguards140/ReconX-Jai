from datetime import datetime


class AuditCore:
    @staticmethod
    def format_log(user_id: str, action: str) -> dict:
        return {"user_id": user_id, "action": action, "timestamp": datetime.now().isoformat()}
