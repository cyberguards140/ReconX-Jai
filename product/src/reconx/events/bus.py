from typing import Callable, Dict, List, Any, Type
import asyncio
from reconx.events.models import BaseEvent
from reconx.logger import setup_logger

logger = setup_logger("EventBus")

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable[[BaseEvent], Any]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.debug(f"Subscribed handler {handler.__name__} to {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable):
        if event_type in self._subscribers and handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)

    async def publish(self, event: BaseEvent):
        if event.event_type in self._subscribers:
            handlers = self._subscribers[event.event_type]
            coroutines = []
            for handler in handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        coroutines.append(handler(event))
                    else:
                        handler(event)
                except Exception as e:
                    logger.error(f"Error dispatching {event.event_type} to {handler.__name__}: {str(e)}")
            
            if coroutines:
                await asyncio.gather(*coroutines, return_exceptions=True)

# Global singleton
event_bus = EventBus()
