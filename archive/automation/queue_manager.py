from core.automation_db import SessionLocal, TaskQueue
from automation.event_bus import EventBus
from dashboard.backend.websocket import broadcast

class QueueManager:
    @staticmethod
    def enqueue(workflow_id):
        db = SessionLocal()
        task = TaskQueue(workflow_id=workflow_id, status="pending")
        db.add(task)
        db.commit()
        db.refresh(task)
        t_id = task.id
        db.close()
        
        broadcast({"type": "job_queued", "task_id": t_id, "workflow_id": workflow_id})
        EventBus.publish("Workflow Queued", {"workflow": workflow_id, "task": t_id})
        return t_id

    @staticmethod
    def list_queue():
        db = SessionLocal()
        tasks = db.query(TaskQueue).all()
        res = [{"id": t.id, "workflow": t.workflow_id, "status": t.status} for t in tasks]
        db.close()
        return res
