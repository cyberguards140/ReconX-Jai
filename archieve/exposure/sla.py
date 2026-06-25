from core.exposure_db import SessionLocal, SLAPolicy

class SLAEngine:
    @staticmethod
    def initialize_policies():
        db = SessionLocal()
        defaults = {"Critical": 7, "High": 30, "Medium": 60, "Low": 90}
        for sev, days in defaults.items():
            if not db.query(SLAPolicy).filter_by(severity=sev).first():
                db.add(SLAPolicy(severity=sev, deadline_days=days))
        db.commit()
        db.close()
