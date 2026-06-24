from core.campaign_db import SessionLocal, CampaignMilestone
from dashboard.backend.websocket import broadcast
from datetime import datetime

class MilestoneManager:
    @staticmethod
    def set_milestone(campaign_id, name, status="Pending"):
        db = SessionLocal()
        m = db.query(CampaignMilestone).filter_by(campaign_id=campaign_id, milestone_name=name).first()
        if not m:
            m = CampaignMilestone(campaign_id=campaign_id, milestone_name=name, status=status)
            db.add(m)
        else:
            m.status = status
            if status == "Completed":
                m.completed_at = datetime.utcnow()
                broadcast({"type": "milestone_completed", "campaign_id": campaign_id, "milestone": name})
        db.commit()
        db.close()
        return True
