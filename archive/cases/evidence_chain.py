from core.case_db import SessionLocal, EvidenceChain
from dashboard.backend.websocket import broadcast
import hashlib

class EvidenceChainEngine:
    @staticmethod
    def log_evidence(case_id, ev_type, source, creator, file_bytes):
        file_hash = hashlib.sha256(file_bytes).hexdigest() if file_bytes else "unknown_hash"
        db = SessionLocal()
        e = EvidenceChain(case_id=case_id, evidence_type=ev_type, file_hash=file_hash, source=source, creator=creator)
        db.add(e)
        db.commit()
        db.refresh(e)
        e_id = e.id
        
        broadcast({"type": "evidence_added", "case_id": case_id, "evidence_id": e_id, "hash": file_hash})
        db.close()
        return e_id
