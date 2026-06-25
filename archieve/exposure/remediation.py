from core.exposure_db import SessionLocal, RemediationAction
from dashboard.backend.websocket import broadcast

class RemediationIntelligence:
    @staticmethod
    def start_remediation(exposure_id, plan_text):
        db = SessionLocal()
        ra = RemediationAction(exposure_id=exposure_id, action_plan=plan_text, status="In Progress")
        db.add(ra)
        db.commit()
        
        broadcast({"type": "remediation_started", "exposure_id": exposure_id})
        db.close()
        return True
