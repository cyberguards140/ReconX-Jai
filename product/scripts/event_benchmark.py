import asyncio
import time
import psutil
import os
import uuid
from reconx.events.bus import EventBus
from reconx.events.models import BaseEvent

async def run_benchmark(num_events: int):
    print(f"\n--- Benchmarking {num_events} Events ---")
    
    bus = EventBus()
    received = 0

    def sync_handler(event: BaseEvent):
        nonlocal received
        received += 1

    bus.subscribe("BenchEvent", sync_handler)

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024
    
    start_time = time.time()
    
    for i in range(num_events):
        event = BaseEvent(
            event_id=str(uuid.uuid4()),
            event_type="BenchEvent",
            correlation_id="bench-corr",
            source="benchmark",
            payload={"index": i}
        )
        await bus.publish(event)
        
    duration = time.time() - start_time
    mem_after = process.memory_info().rss / 1024 / 1024
    
    print(f"Events Handled: {received}")
    print(f"Execution Time: {duration:.4f} seconds")
    print(f"Throughput: {num_events / duration:.2f} events/sec")
    print(f"Memory Diff: {mem_after - mem_before:.2f} MB")
    
if __name__ == "__main__":
    asyncio.run(run_benchmark(100))
    asyncio.run(run_benchmark(1000))
    asyncio.run(run_benchmark(10000))
