from core.auth_db import SessionLocal, ActivityLog

class ActivityTracker:
    @staticmethod
    def log_activity(user_id, action):
        db = SessionLocal()
        log = ActivityLog(user_id=user_id, action=action)
        db.add(log)
        db.commit()
        db.close()
