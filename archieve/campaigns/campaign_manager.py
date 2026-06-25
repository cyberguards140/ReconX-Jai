from core.campaign_db import SessionLocal, Campaign
from dashboard.backend.websocket import broadcast

class CampaignManager:
    @staticmethod
    def create_campaign(name, campaign_type):
        db = SessionLocal()
        c = Campaign(name=name, campaign_type=campaign_type)
        db.add(c)
        db.commit()
        db.refresh(c)
        c_id = c.id
        
        broadcast({"type": "campaign_created", "campaign_id": c_id, "name": name})
        db.close()
        return c_id

    @staticmethod
    def get_campaigns():
        db = SessionLocal()
        res = db.query(Campaign).all()
        data = [{"id": c.id, "name": c.name, "type": c.campaign_type, "status": c.status} for c in res]
        db.close()
        return data
