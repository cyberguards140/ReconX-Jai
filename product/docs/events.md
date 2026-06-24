# Event Bus Architecture

ReconX uses an async-native Publish/Subscribe architecture to coordinate state changes, audit logging, and plugin coordination across the platform decoupled from the execution loop.

## Core Components

- **EventBus (`src/reconx/events/bus.py`)**: A high-performance singleton holding async subscriber callbacks.
- **Models (`src/reconx/events/models.py`)**: Strictly validated Pydantic events ensuring `correlation_id` and timestamp guarantees.
- **Handlers (`src/reconx/events/handlers.py`)**: Dedicated listeners that consume events for distinct downstream effects (Logging, Metrics, and DB Persistence).

## Event Models

Every event inherits from `BaseEvent` which enforces:
- `event_id`: A unique UUID.
- `event_type`: String identifier (e.g., `WorkflowCompleted`).
- `timestamp`: UTC datetime.
- `correlation_id`: The workflow trace ID used to piece together distributed logs.
- `source`: Emitter source name.
- `payload`: Flexible JSON blob.

## Handlers

1. **LoggingHandler**: Consumes all workflow and task events to produce unified, correlation-id tagged JSON logs.
2. **MetricsHandler**: Plugs into `reconx.metrics.registry.py` updating Prometheus Counters upon successes and failures.
3. **PersistenceHandler**: Translates events directly into `EventLog` SQL records.

## Usage

```python
from reconx.events.bus import event_bus
from reconx.events.models import WorkflowEvent

await event_bus.publish(WorkflowEvent(
    event_id=uuid.uuid4(),
    event_type="WorkflowStarted",
    correlation_id="wf-123",
    source="my_module"
))
```
