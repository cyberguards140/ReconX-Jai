from core.analytics_db import SessionLocal, HistoricalSnapshot
from dashboard.backend.websocket import broadcast
import random

class SnapshotEngine:
    @staticmethod
    def generate_snapshot(project_id):
        # Simulated snapshot logic fetching from intelligence.db
        total_assets = random.randint(100, 1500)
        total_findings = random.randint(10, 200)
        critical_findings = random.randint(0, 15)
        risk_score = random.uniform(30.0, 95.0)
        
        db = SessionLocal()
        snap = HistoricalSnapshot(
            project_id=project_id,
            total_assets=total_assets,
            total_findings=total_findings,
            critical_findings=critical_findings,
            risk_score=risk_score
        )
        db.add(snap)
        db.commit()
        
        broadcast({
            "type": "snapshot_created",
            "project_id": project_id,
            "total_assets": total_assets
        })
        db.close()
        return True
