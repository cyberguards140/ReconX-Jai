"""Job queue for async worker processing."""

import asyncio
from typing import Any


class JobQueue:
    """Priority-based async job queue."""

    def __init__(self):
        self.queue: asyncio.PriorityQueue[tuple[int, Any]] = asyncio.PriorityQueue()

    async def enqueue(self, job: Any, priority: int = 5) -> None:
        """Add a job to the queue with the given priority (lower = higher priority)."""
        await self.queue.put((priority, job))

    async def dequeue(self) -> tuple[int, Any]:
        """Get the next job from the queue."""
        return await self.queue.get()

    def qsize(self) -> int:
        """Return the current queue size."""
        return self.queue.qsize()


# Singleton instance
job_queue = JobQueue()
