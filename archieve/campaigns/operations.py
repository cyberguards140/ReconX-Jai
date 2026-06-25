from core.campaign_db import SessionLocal, CampaignTask
from dashboard.backend.websocket import broadcast

class TaskManager:
    @staticmethod
    def create_task(campaign_id, name, task_type, assigned_to=None):
        db = SessionLocal()
        t = CampaignTask(campaign_id=campaign_id, task_name=name, task_type=task_type, assigned_to=assigned_to)
        db.add(t)
        db.commit()
        db.refresh(t)
        t_id = t.id
        
        if assigned_to:
            broadcast({"type": "task_assigned", "campaign_id": campaign_id, "task_id": t_id, "user": assigned_to})
        db.close()
        return t_id
