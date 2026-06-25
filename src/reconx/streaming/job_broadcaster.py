import json

from .event_dispatcher import event_dispatcher


class JobBroadcaster:
    @staticmethod
    async def broadcast_status(job_id, status):
        event = {"type": "status", "job_id": job_id, "status": status}
        await event_dispatcher.dispatch("/ws/jobs", json.dumps(event))
