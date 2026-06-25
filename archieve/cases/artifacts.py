from core.case_db import SessionLocal, Artifact
from dashboard.backend.websocket import broadcast

class ArtifactManager:
    @staticmethod
    def store_artifact(case_id, name, artifact_type, path):
        db = SessionLocal()
        a = Artifact(case_id=case_id, artifact_name=name, artifact_type=artifact_type, file_path=path)
        db.add(a)
        db.commit()
        db.refresh(a)
        a_id = a.id
        
        broadcast({"type": "artifact_generated", "case_id": case_id, "artifact_id": a_id})
        db.close()
        return a_id
