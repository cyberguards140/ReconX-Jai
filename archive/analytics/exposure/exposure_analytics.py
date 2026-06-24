from core.analytics_db import SessionLocal, ExposureMetric
from dashboard.backend.websocket import broadcast
import random

class ExposureAnalytics:
    @staticmethod
    def calculate_exposure(project_id):
        db = SessionLocal()
        # Simulated calculation
        score = random.uniform(20.0, 85.0)
        exp = ExposureMetric(project_id=project_id, exposure_score=score)
        db.add(exp)
        db.commit()
        
        broadcast({
            "type": "exposure_changed",
            "project_id": project_id,
            "score": score
        })
        db.close()
        return score
