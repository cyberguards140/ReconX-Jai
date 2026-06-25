from core.analytics_db import SessionLocal, ForecastData
from dashboard.backend.websocket import broadcast
from datetime import datetime, timedelta

class ForecastEngine:
    @staticmethod
    def generate_forecast(project_id, category, projected_value, days_ahead=30):
        db = SessionLocal()
        target = datetime.utcnow() + timedelta(days=days_ahead)
        f = ForecastData(
            project_id=project_id,
            forecast_category=category,
            projected_value=projected_value,
            target_date=target
        )
        db.add(f)
        db.commit()
        
        broadcast({
            "type": "forecast_generated",
            "project_id": project_id,
            "category": category
        })
        db.close()
        return True
