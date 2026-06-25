import json

from data.database.session import async_session_factory
from core.events.models import BaseEvent, TaskEvent
from core.logging.logger import setup_logger
from observability.metrics.registry import metrics_registry

logger = setup_logger("EventHandlers")


class LoggingHandler:
    @staticmethod
    def handle(event: BaseEvent):
        # Structured logging
        extra = {
            "event_id": event.event_id,
            "correlation_id": event.correlation_id,
            "source": event.source,
        }
        if isinstance(event, TaskEvent):
            extra["task_id"] = event.task_id

        logger.info(event.event_type, extra=extra)


class MetricsHandler:
    @staticmethod
    def handle(event: BaseEvent):
        if event.event_type == "WorkflowCompleted":
            metrics_registry.increment("workflows_completed")
        elif event.event_type == "WorkflowFailed":
            metrics_registry.increment("workflows_failed")
        elif event.event_type == "TaskCompleted":
            metrics_registry.increment("tasks_completed")
        elif event.event_type == "TaskFailed":
            metrics_registry.increment("tasks_failed")


class PersistenceHandler:
    @staticmethod
    async def handle(event: BaseEvent):
        # Save event to EventLog table
        from data.database.models import EventLog

        async with async_session_factory() as db:
            db.add(
                EventLog(
                    event_type=event.event_type,
                    timestamp=event.timestamp,
                    correlation_id=event.correlation_id,
                    payload=json.dumps(event.payload),
                )
            )
            await db.commit()


def register_handlers(bus):
    # Core system events to log
    all_events = [
        "WorkflowStarted",
        "WorkflowCompleted",
        "WorkflowFailed",
        "WorkflowCancelled",
        "TaskStarted",
        "TaskCompleted",
        "TaskFailed",
        "TaskCancelled",
        "TaskSkipped",
    ]
    for e in all_events:
        bus.subscribe(e, LoggingHandler.handle)
        bus.subscribe(e, MetricsHandler.handle)
        bus.subscribe(e, PersistenceHandler.handle)
