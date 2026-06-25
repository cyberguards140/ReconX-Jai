from core.analytics_db import SessionLocal, TrendData
from dashboard.backend.websocket import broadcast

class TrendEngine:
    @staticmethod
    def calculate_trend(project_id, category, delta, description):
        db = SessionLocal()
        t = TrendData(
            project_id=project_id,
            trend_category=category,
            delta_value=delta,
            description=description
        )
        db.add(t)
        db.commit()
        
        broadcast({
            "type": "trend_updated",
            "project_id": project_id,
            "category": category,
            "delta": delta
        })
        db.close()
        return True
