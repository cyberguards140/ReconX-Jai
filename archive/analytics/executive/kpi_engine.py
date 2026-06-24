from core.analytics_db import SessionLocal, ExecutiveMetric
from dashboard.backend.websocket import broadcast

class KPIEngine:
    @staticmethod
    def log_kpi(project_id, name, value):
        db = SessionLocal()
        kpi = ExecutiveMetric(project_id=project_id, metric_name=name, metric_value=value)
        db.add(kpi)
        db.commit()
        
        broadcast({
            "type": "kpi_updated",
            "project_id": project_id,
            "metric": name,
            "value": value
        })
        db.close()
        return True
