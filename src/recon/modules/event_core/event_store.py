import logging

from recon.modules.event_core.event_types import SystemEvent

logger = logging.getLogger(__name__)


class EventStore:
    """
    Intelligence Memory: Stores event history, allows for replay.
    Abstracts over the database EventLog model.
    """

    def __init__(self, db_session=None):
        self.db = db_session
        self._in_memory_log: list[SystemEvent] = []

    def store_event(self, event: SystemEvent):
        """Persist the event to storage."""
        # For structural implementation without active DB dependency, use memory
        self._in_memory_log.append(event)

        if self.db:
            # Here we would map to the SQLAlchemy EventLog model
            pass

        logger.debug(f"Event stored: {event.event_id}")

    def get_events(self, event_type: str | None = None) -> list[SystemEvent]:
        """Retrieve events, optionally filtered by type."""
        if event_type:
            return [e for e in self._in_memory_log if e.event_type == event_type]
        return self._in_memory_log

    def replay_events(self, bus, event_type: str | None = None):
        """Replay past intelligence events into the bus."""
        events = self.get_events(event_type)
        logger.info(f"Replaying {len(events)} events.")
        for event in events:
            bus.publish(event)
