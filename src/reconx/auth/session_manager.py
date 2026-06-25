from core.auth_db import Session, SessionLocal


class SessionManager:
    @staticmethod
    def create_session(user_id, ip_address="127.0.0.1", device="CLI"):
        db = SessionLocal()
        s = Session(user_id=user_id, ip_address=ip_address, device=device)
        db.add(s)
        db.commit()
        db.refresh(s)
        s_id = s.id
        db.close()
        return s_id

    @staticmethod
    def revoke_session(session_id):
        db = SessionLocal()
        s = db.query(Session).filter(Session.id == session_id).first()
        if s:
            s.status = "Revoked"
            db.commit()
        db.close()
