from core.auth_db import ApprovalRequest, SessionLocal
from dashboard.backend.websocket import broadcast


class ApprovalEngine:
    @staticmethod
    def request_approval(user_id, action):
        db = SessionLocal()
        ar = ApprovalRequest(user_id=user_id, action=action)
        db.add(ar)
        db.commit()
        db.refresh(ar)

        broadcast({"type": "approval_requested", "request_id": ar.id, "action": action})

        db.close()
        return ar.id
