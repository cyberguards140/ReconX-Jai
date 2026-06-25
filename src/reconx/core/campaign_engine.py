from core.project_db import SessionLocal, Campaign
from dashboard.backend.websocket import broadcast

class CampaignEngine:
    @staticmethod
    def start_campaign(project_id, name, type_label="Recon Campaign"):
        db = SessionLocal()
        camp = Campaign(project_id=project_id, name=name, status="running")
        db.add(camp)
        db.commit()
        db.refresh(camp)
        c_id = camp.id
        db.close()
        
        msg = {
            "type": "campaign_started",
            "project_id": project_id,
            "campaign_id": c_id,
            "campaign_name": name
        }
        broadcast(msg)
        return c_id

    @staticmethod
    def stop_campaign(campaign_id):
        db = SessionLocal()
        camp = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if camp:
            camp.status = "completed"
            db.commit()
            
            msg = {
                "type": "campaign_completed",
                "campaign_id": campaign_id
            }
            broadcast(msg)
        db.close()
