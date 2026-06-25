from core.case_db import SessionLocal, Case

class InvestigationAnalytics:
    @staticmethod
    def get_metrics():
        db = SessionLocal()
        open_cases = db.query(Case).filter(Case.status != "Closed").count()
        closed_cases = db.query(Case).filter(Case.status == "Closed").count()
        db.close()
        return {"open_cases": open_cases, "closed_cases": closed_cases, "average_resolution_time_days": 2.5}
