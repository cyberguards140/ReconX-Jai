from core.campaign_db import SessionLocal, Evidence
from dashboard.backend.websocket import broadcast
from campaigns.timeline import TimelineEngine

class EvidenceManager:
    @staticmethod
    def log_evidence(campaign_id, ev_type, path):
        db = SessionLocal()
        e = Evidence(campaign_id=campaign_id, evidence_type=ev_type, file_path=path)
        db.add(e)
        db.commit()
        db.refresh(e)
        e_id = e.id
        
        broadcast({"type": "evidence_uploaded", "campaign_id": campaign_id, "evidence_id": e_id})
        db.close()
        
        TimelineEngine.log_event(campaign_id, f"Evidence uploaded: {path}")
        return e_id
