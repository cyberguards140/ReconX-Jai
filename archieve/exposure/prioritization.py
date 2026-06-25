from core.exposure_db import SessionLocal, Exposure, RiskScore

class PrioritizationEngine:
    @staticmethod
    def get_priority_queue(project_id):
        db = SessionLocal()
        # Retrieve all open exposures sorted by their latest risk score
        exposures = db.query(Exposure).filter_by(project_id=project_id, status="Open").all()
        # Mocking sorting
        db.close()
        return sorted([{"id": e.id, "severity": e.severity} for e in exposures], key=lambda x: x["severity"], reverse=True)
