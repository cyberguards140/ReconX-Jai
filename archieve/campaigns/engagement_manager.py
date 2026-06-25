from core.campaign_db import SessionLocal, Engagement

class EngagementManager:
    @staticmethod
    def create_engagement(campaign_id, name, client):
        db = SessionLocal()
        e = Engagement(campaign_id=campaign_id, engagement_name=name, client=client)
        db.add(e)
        db.commit()
        db.refresh(e)
        e_id = e.id
        db.close()
        return e_id
