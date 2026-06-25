import json

from .event_dispatcher import event_dispatcher


class TerminalStream:
    @staticmethod
    async def broadcast_output(job_id, stream_type, message):
        event = {
            "type": stream_type,  # 'stdout', 'stderr', 'error', 'success'
            "job_id": job_id,
            "message": message,
        }
        await event_dispatcher.dispatch("/ws/terminal", json.dumps(event))
