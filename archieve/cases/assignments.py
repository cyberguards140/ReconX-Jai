from core.case_db import SessionLocal, CaseAssignment
from dashboard.backend.websocket import broadcast

class AssignmentEngine:
    @staticmethod
    def assign_case(case_id, assignee, assign_type="User"):
        db = SessionLocal()
        a = CaseAssignment(case_id=case_id, assignee=assignee, assignment_type=assign_type)
        db.add(a)
        db.commit()
        
        broadcast({"type": "case_assigned", "case_id": case_id, "assignee": assignee})
        db.close()
        return True
