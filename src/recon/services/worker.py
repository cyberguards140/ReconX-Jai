import asyncio
import logging
import uuid
import socket
from typing import Dict, Any
from core.messaging.broker import broker
from core.messaging.worker_registry import worker_registry

logger = logging.getLogger(__name__)

class ReconWorker:
    """
    Remote worker daemon. Pulls tasks from the global broker, executes local tool paths,
    and pushes results to the results_queue.
    """
    def __init__(self, queues_to_watch: list[str] = ["httpx", "naabu", "dnsx"]):
        self.worker_id = f"worker-{uuid.uuid4().hex[:8]}"
        self.hostname = socket.gethostname()
        self.queues = queues_to_watch
        self.running = False
        
    async def start(self):
        self.running = True
        # Register self
        worker_registry.register_worker(self.worker_id, self.hostname)
        logger.info(f"Worker {self.worker_id} started on {self.hostname}. Watching {self.queues}")
        
        # Start background task loops
        tasks = []
        for q in self.queues:
            tasks.append(asyncio.create_task(self._consume_loop(q)))
        
        # Heartbeat loop
        tasks.append(asyncio.create_task(self._heartbeat_loop()))
        
        await asyncio.gather(*tasks)
        
    async def _heartbeat_loop(self):
        while self.running:
            worker_registry.heartbeat(self.worker_id, "active")
            await asyncio.sleep(30)
            
    async def _consume_loop(self, queue_name: str):
        while self.running:
            # This is a blocking pull
            task_payload = await broker.consume(queue_name)
            logger.info(f"[{self.worker_id}] Processing task from {queue_name}: {task_payload}")
            
            # Execute tool logic here (simulate)
            await asyncio.sleep(1)
            
            # Push result back to centralized queue
            result_payload = {
                "worker_id": self.worker_id,
                "original_task": task_payload,
                "status": "completed",
                "stage": queue_name
            }
            await broker.publish("store_results", result_payload)
