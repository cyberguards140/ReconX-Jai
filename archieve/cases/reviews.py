from core.case_db import SessionLocal, CaseReview
from dashboard.backend.websocket import broadcast
from datetime import datetime

class ReviewEngine:
    @staticmethod
    def submit_review(case_id, reviewer, status="Approved"):
        db = SessionLocal()
        r = CaseReview(case_id=case_id, reviewer=reviewer, status=status, reviewed_at=datetime.utcnow())
        db.add(r)
        db.commit()
        
        broadcast({"type": "review_submitted", "case_id": case_id, "reviewer": reviewer, "status": status})
        db.close()
        return True
