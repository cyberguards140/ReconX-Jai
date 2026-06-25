from core.graph_db import SessionLocal, AttackPath
from dashboard.backend.websocket import broadcast
import json

class AttackPathEngine:
    @staticmethod
    def model_path(project_id, path_nodes_list, risk_score):
        db = SessionLocal()
        ap = AttackPath(
            project_id=project_id,
            path_details=json.dumps(path_nodes_list),
            risk_score=risk_score
        )
        db.add(ap)
        db.commit()
        
        broadcast({
            "type": "attack_path_updated",
            "project_id": project_id,
            "score": risk_score
        })
        db.close()
        return True
