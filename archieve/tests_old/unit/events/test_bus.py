import pytest
import asyncio
from reconx.events.bus import EventBus
from reconx.events.models import BaseEvent

@pytest.mark.asyncio
async def test_publish_subscribe():
    bus = EventBus()
    received = []

    def sync_handler(event: BaseEvent):
        received.append("sync")

    async def async_handler(event: BaseEvent):
        await asyncio.sleep(0.01)
        received.append("async")

    bus.subscribe("TestEvent", sync_handler)
    bus.subscribe("TestEvent", async_handler)

    event = BaseEvent(
        event_id="1",
        event_type="TestEvent",
        correlation_id="test-corr",
        source="test",
        payload={"data": "test"}
    )

    await bus.publish(event)
    
    assert len(received) == 2
    assert "sync" in received
    assert "async" in received

@pytest.mark.asyncio
async def test_unsubscribe():
    bus = EventBus()
    received = []

    def sync_handler(event: BaseEvent):
        received.append("sync")

    bus.subscribe("TestEvent", sync_handler)
    bus.unsubscribe("TestEvent", sync_handler)

    event = BaseEvent(
        event_id="1",
        event_type="TestEvent",
        correlation_id="test-corr",
        source="test",
        payload={}
    )

    await bus.publish(event)
    assert len(received) == 0
