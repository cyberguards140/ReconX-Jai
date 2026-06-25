from core.campaign_db import SessionLocal, CampaignTimeline

class TimelineEngine:
    @staticmethod
    def log_event(campaign_id, description):
        db = SessionLocal()
        t = CampaignTimeline(campaign_id=campaign_id, event_description=description)
        db.add(t)
        db.commit()
        db.close()
        return True
