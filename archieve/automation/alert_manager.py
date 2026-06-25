from core.automation_db import SessionLocal, Alert
from dashboard.backend.websocket import broadcast

class AlertManager:
    @staticmethod
    def handle_event(event):
        # Determine if event warrants an alert
        critical_events = ["Critical Vulnerability", "New Asset Discovered", "Cloud Exposure", "Workflow Failure"]
        if event.get("event") in critical_events:
            AlertManager.create_alert(
                project_id=event.get("project_id", "system"),
                alert_type=event.get("event"),
                message=event.get("message", "An automated event occurred."),
                severity=event.get("severity", "medium")
            )

    @staticmethod
    def create_alert(project_id, alert_type, message, severity):
        db = SessionLocal()
        al = Alert(project_id=project_id, alert_type=alert_type, message=message, severity=severity)
        db.add(al)
        db.commit()
        db.refresh(al)
        
        # Broadcast to dashboard
        msg = {
            "type": "alert_generated",
            "alert_id": al.id,
            "alert_type": alert_type,
            "message": message,
            "severity": severity
        }
        broadcast(msg)
        db.close()

    @staticmethod
    def get_unread(project_id):
        db = SessionLocal()
        alerts = db.query(Alert).filter(Alert.project_id == project_id, Alert.read == False).all()
        res = [{"id": a.id, "type": a.alert_type, "message": a.message, "severity": a.severity} for a in alerts]
        db.close()
        return res

# Subscribe to bus implicitly inside the engine.
