import asyncio
import logging
import json
from typing import Dict, Any, Callable, Awaitable

logger = logging.getLogger(__name__)

class MessageBroker:
    """
    Abstracted Message Broker interface.
    Currently simulating Redis/RabbitMQ via asyncio for MVP.
    """
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        self.subscribers: Dict[str, list[Callable[[Dict[str, Any]], Awaitable[None]]]] = {}

    def _get_queue(self, queue_name: str) -> asyncio.Queue:
        if queue_name not in self.queues:
            self.queues[queue_name] = asyncio.Queue()
        return self.queues[queue_name]

    async def publish(self, queue_name: str, payload: Dict[str, Any]):
        """Push a task to a specific queue."""
        queue = self._get_queue(queue_name)
        await queue.put(json.dumps(payload))
        logger.debug(f"Published task to {queue_name}")

    async def consume(self, queue_name: str) -> Dict[str, Any]:
        """Pull a task from a specific queue (blocking)."""
        queue = self._get_queue(queue_name)
        raw_payload = await queue.get()
        return json.loads(raw_payload)

    def subscribe(self, queue_name: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]):
        """Register a callback for when a task is pulled."""
        if queue_name not in self.subscribers:
            self.subscribers[queue_name] = []
        self.subscribers[queue_name].append(callback)

    async def start_consumer(self, queue_name: str):
        """Start a background loop to consume messages and fire callbacks."""
        queue = self._get_queue(queue_name)
        while True:
            raw_payload = await queue.get()
            payload = json.loads(raw_payload)
            if queue_name in self.subscribers:
                for callback in self.subscribers[queue_name]:
                    try:
                        await callback(payload)
                    except Exception as e:
                        logger.error(f"Callback failed on {queue_name}: {e}")
            queue.task_done()

# Singleton broker instance
broker = MessageBroker()
