import logging
from collections.abc import Callable

from reconx.modules.event_core.event_types import SystemEvent

logger = logging.getLogger(__name__)


class EventRouter:
    """
    Routes events intelligently to specific dispatcher queues based on rules.
    """

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self._rules = []

    def add_routing_rule(self, condition: Callable[[SystemEvent], bool], target_queue: str):
        """Add a rule: if condition(event) is True, route to target_queue."""
        self._rules.append((condition, target_queue))

    def route_event(self, event: SystemEvent):
        """Evaluate event against rules and route it."""
        routed = False
        for condition, target_queue in self._rules:
            if condition(event):
                logger.info(f"Routing {event.event_id} to queue: {target_queue}")
                self.dispatcher.enqueue(event, target_queue)
                routed = True

        if not routed:
            logger.debug(f"Event {event.event_id} not routed to any specific queue.")
