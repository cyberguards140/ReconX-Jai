import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger(__name__)


class MessageBroker:
    """
    Abstracted Message Broker interface.
    Currently simulating Redis/RabbitMQ via asyncio for MVP.
    """

    def __init__(self):
        self.queues: dict[str, asyncio.Queue] = {}
        self.subscribers: dict[str, list[Callable[[dict[str, Any]], Awaitable[None]]]] = {}

    def _get_queue(self, queue_name: str) -> asyncio.Queue:
        if queue_name not in self.queues:
            self.queues[queue_name] = asyncio.Queue()
        return self.queues[queue_name]

    async def publish(self, queue_name: str, payload: dict[str, Any]):
        """Push a task to a specific queue."""
        queue = self._get_queue(queue_name)
        await queue.put(json.dumps(payload))
        logger.debug(f"Published task to {queue_name}")

    async def consume(self, queue_name: str) -> dict[str, Any]:
        """Pull a task from a specific queue (blocking)."""
        queue = self._get_queue(queue_name)
        raw_payload = await queue.get()
        return json.loads(raw_payload)

    def subscribe(self, queue_name: str, callback: Callable[[dict[str, Any]], Awaitable[None]]):
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
