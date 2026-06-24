from core.campaign_db import SessionLocal, AssessmentScope
from dashboard.backend.websocket import broadcast

class ScopeManager:
    @staticmethod
    def add_scope(campaign_id, target, status="In Scope"):
        db = SessionLocal()
        s = AssessmentScope(campaign_id=campaign_id, target=target, status=status)
        db.add(s)
        db.commit()
        db.refresh(s)
        s_id = s.id
        
        broadcast({"type": "scope_updated", "campaign_id": campaign_id, "target": target, "status": status})
        db.close()
        return s_id

    @staticmethod
    def validate_target(campaign_id, target):
        db = SessionLocal()
        s = db.query(AssessmentScope).filter_by(campaign_id=campaign_id, target=target, status="In Scope").first()
        db.close()
        return s is not None
