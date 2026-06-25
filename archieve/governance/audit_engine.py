from core.auth_db import SessionLocal, AuditLog

class AuditEngine:
    @staticmethod
    def log_audit_event(user_id, event, details):
        db = SessionLocal()
        log = AuditLog(user_id=user_id, event=event, details=details)
        db.add(log)
        db.commit()
        db.close()
