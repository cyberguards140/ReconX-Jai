from core.analytics_db import SessionLocal, RiskMetric
from dashboard.backend.websocket import broadcast
import random

class RiskAnalytics:
    @staticmethod
    def calculate_risk(project_id):
        db = SessionLocal()
        score = random.uniform(10.0, 95.0)
        rm = RiskMetric(project_id=project_id, risk_score=score)
        db.add(rm)
        db.commit()
        
        broadcast({
            "type": "risk_updated",
            "project_id": project_id,
            "score": score
        })
        db.close()
        return score
