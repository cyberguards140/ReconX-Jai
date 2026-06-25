from auth.password_manager import PasswordManager
from auth.session_manager import SessionManager
from core.auth_db import SessionLocal, User
from dashboard.backend.websocket import broadcast
from governance.activity_tracker import ActivityTracker


class AuthenticationEngine:
    @staticmethod
    def login(username, password, ip_address="127.0.0.1"):
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()

        if user and PasswordManager.verify_password(password, user.password_hash):
            if user.status != "Active":
                db.close()
                return False, "Account is not active."

            session_id = SessionManager.create_session(user.id, ip_address)
            ActivityTracker.log_activity(user.id, "Logged In")

            broadcast({"type": "user_logged_in", "user_id": user.id, "username": user.username})

            db.close()
            return True, session_id

        db.close()
        return False, "Invalid credentials."

    @staticmethod
    def logout(session_id, user_id):
        SessionManager.revoke_session(session_id)
        ActivityTracker.log_activity(user_id, "Logged Out")
        return True
