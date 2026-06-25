from recon.modules.enterprise.audit import AuditCore


class AuditLogService:
    def __init__(self):
        self.logs = []

    def log_action(self, user_id: str, action: str):
        entry = AuditCore.format_log(user_id, action)
        self.logs.append(entry)
