import logging
from collections.abc import Callable

from recon.modules.event_core.event_types import SystemEvent

logger = logging.getLogger(__name__)


class EventBus:
    """
    Central communication layer for publishing and subscribing to system events.
    """

    def __init__(self):
        self._subscribers: dict[str, list[Callable[[SystemEvent], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[SystemEvent], None]):
        """Register a callback for a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to {event_type}")

    def publish(self, event: SystemEvent):
        """Publish an event to all registered subscribers."""
        logger.info(f"Publishing event: {event.event_type} [{event.event_id}]")

        # Exact match subscribers
        if event.event_type in self._subscribers:
            for callback in self._subscribers[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in subscriber for {event.event_type}: {e}")

        # Wildcard subscribers
        if "*" in self._subscribers:
            for callback in self._subscribers["*"]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in wildcard subscriber: {e}")
