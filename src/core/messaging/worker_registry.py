import time
from typing import Dict, Any

class WorkerRegistry:
    """
    Tracks active scanning nodes (workers) across the distributed fleet.
    """
    def __init__(self):
        self.workers: Dict[str, Dict[str, Any]] = {}

    def register_worker(self, worker_id: str, hostname: str):
        self.workers[worker_id] = {
            "hostname": hostname,
            "status": "idle",
            "last_heartbeat": time.time(),
            "tasks_completed": 0
        }

    def heartbeat(self, worker_id: str, status: str):
        if worker_id in self.workers:
            self.workers[worker_id]["last_heartbeat"] = time.time()
            self.workers[worker_id]["status"] = status

    def get_active_workers(self, timeout_seconds: int = 60) -> list[Dict[str, Any]]:
        current_time = time.time()
        active = []
        for wid, data in self.workers.items():
            if current_time - data["last_heartbeat"] < timeout_seconds:
                active.append({"worker_id": wid, **data})
        return active

worker_registry = WorkerRegistry()
