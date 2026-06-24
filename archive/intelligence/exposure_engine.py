from core.threat_db import SessionLocal, ExposureEvent
from dashboard.backend.websocket import broadcast

class ExposureEngine:
    @staticmethod
    def log_exposure(asset_id, event_type):
        db = SessionLocal()
        exp = ExposureEvent(asset_id=asset_id, event_type=event_type)
        db.add(exp)
        db.commit()
        db.close()
        
        broadcast({
            "type": "exposure_detected",
            "asset_id": asset_id,
            "event_type": event_type
        })
        return True
