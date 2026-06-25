from core.exposure_db import SessionLocal, SecurityPosture
from dashboard.backend.websocket import broadcast
import random

class SecurityPostureEngine:
    @staticmethod
    def calculate_posture(project_id):
        db = SessionLocal()
        # Simulated calculation
        score = random.uniform(50.0, 98.0)
        grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
        
        sp = SecurityPosture(project_id=project_id, score=score, grade=grade)
        db.add(sp)
        db.commit()
        
        broadcast({"type": "posture_updated", "project_id": project_id, "score": score, "grade": grade})
        db.close()
        return {"score": score, "grade": grade}
