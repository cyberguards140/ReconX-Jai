from core.case_db import SessionLocal, CaseTimeline

class CaseTimelineEngine:
    @staticmethod
    def log_event(case_id, description):
        db = SessionLocal()
        t = CaseTimeline(case_id=case_id, event_description=description)
        db.add(t)
        db.commit()
        db.close()
        return True
