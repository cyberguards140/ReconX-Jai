import logging
import queue
from typing import Dict, Callable
from reconx.modules.event_core.event_types import SystemEvent

logger = logging.getLogger(__name__)

class EventDispatcher:
    """
    Handles execution logic: Event -> Trigger -> Module -> Result -> New Event.
    """
    def __init__(self, bus):
        self.bus = bus
        self._queues: Dict[str, queue.Queue] = {
            "asm_engine": queue.Queue(),
            "infra_engine": queue.Queue(),
            "analytics_engine": queue.Queue(),
            "background": queue.Queue()
        }
        self._handlers: Dict[str, Callable[[SystemEvent], None]] = {}

    def register_handler(self, target_queue: str, handler: Callable[[SystemEvent], None]):
        """Register the worker logic for a specific queue."""
        self._handlers[target_queue] = handler

    def enqueue(self, event: SystemEvent, target_queue: str):
        """Place an event into a queue based on prioritization."""
        if target_queue not in self._queues:
            self._queues[target_queue] = queue.Queue()
        
        self._queues[target_queue].put(event)
        
        # In a real async system, workers would pull from the queue.
        # Here we mimic synchronous dispatch for structural demonstration.
        self._process_queue(target_queue)

    def _process_queue(self, target_queue: str):
        """Process items in a queue."""
        q = self._queues[target_queue]
        handler = self._handlers.get(target_queue)
        
        while not q.empty():
            event = q.get()
            if handler:
                try:
                    logger.debug(f"Dispatching {event.event_id} to {target_queue}")
                    handler(event)
                except Exception as e:
                    logger.error(f"Handler failed for queue {target_queue}: {e}")
            q.task_done()
