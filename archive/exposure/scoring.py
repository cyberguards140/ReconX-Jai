from core.exposure_db import SessionLocal, RiskScore, Exposure, BusinessCriticality
from dashboard.backend.websocket import broadcast
import random

class ScoringEngine:
    @staticmethod
    def calculate_risk(exposure_id):
        db = SessionLocal()
        exp = db.query(Exposure).filter_by(id=exposure_id).first()
        if not exp:
            db.close()
            return 0.0
            
        base_scores = {"Informational": 10.0, "Low": 30.0, "Medium": 50.0, "High": 75.0, "Critical": 95.0}
        score = base_scores.get(exp.severity, 0.0)
        
        # Apply business criticality multiplier
        bc = db.query(BusinessCriticality).filter_by(asset_id=exp.asset_id).first()
        if bc and bc.criticality == "Critical":
            score = min(score * 1.2, 100.0)
            
        rs = RiskScore(exposure_id=exposure_id, score=score)
        db.add(rs)
        db.commit()
        
        broadcast({"type": "risk_updated", "exposure_id": exposure_id, "score": score})
        db.close()
        return score
