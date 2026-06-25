from core.case_db import SessionLocal, Investigation

class InvestigationWorkspace:
    @staticmethod
    def create_investigation(case_id, name, owner):
        db = SessionLocal()
        i = Investigation(case_id=case_id, investigation_name=name, owner=owner)
        db.add(i)
        db.commit()
        db.refresh(i)
        i_id = i.id
        db.close()
        return i_id
