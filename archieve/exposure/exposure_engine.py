from core.exposure_db import SessionLocal, Exposure
from dashboard.backend.websocket import broadcast

class ExposureEngine:
    @staticmethod
    def create_exposure(project_id, asset_id, exposure_type, severity):
        db = SessionLocal()
        e = Exposure(project_id=project_id, asset_id=asset_id, exposure_type=exposure_type, severity=severity)
        db.add(e)
        db.commit()
        db.refresh(e)
        
        broadcast({"type": "exposure_created", "project_id": project_id, "exposure_id": e.id})
        db.close()
        return e.id
