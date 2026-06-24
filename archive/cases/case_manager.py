from core.case_db import SessionLocal, Case
from dashboard.backend.websocket import broadcast

class CaseManager:
    @staticmethod
    def create_case(title, case_type):
        db = SessionLocal()
        c = Case(title=title, case_type=case_type)
        db.add(c)
        db.commit()
        db.refresh(c)
        c_id = c.id
        
        broadcast({"type": "case_created", "case_id": c_id, "title": title})
        db.close()
        return c_id

    @staticmethod
    def get_cases():
        db = SessionLocal()
        res = db.query(Case).all()
        data = [{"id": c.id, "title": c.title, "type": c.case_type, "status": c.status} for c in res]
        db.close()
        return data
