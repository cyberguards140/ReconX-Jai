from core.intelligence_db import SessionLocal, AssetTimeline
from dashboard.backend.websocket import broadcast

class TimelineEngine:
    @staticmethod
    def log_event(asset_id, event_type, message):
        db = SessionLocal()
        tl = AssetTimeline(asset_id=asset_id, event_type=event_type, message=message)
        db.add(tl)
        db.commit()
        db.close()
        
        broadcast({
            "type": "timeline_event",
            "asset_id": asset_id,
            "event_type": event_type,
            "message": message
        })
