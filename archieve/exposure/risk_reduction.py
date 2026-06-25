from core.exposure_db import SessionLocal, RiskReduction

class RiskReductionTracker:
    @staticmethod
    def track_reduction(project_id, percentage):
        db = SessionLocal()
        rr = RiskReduction(project_id=project_id, reduction_percentage=percentage)
        db.add(rr)
        db.commit()
        db.close()
        return True
