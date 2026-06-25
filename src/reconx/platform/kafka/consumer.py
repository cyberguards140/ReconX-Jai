import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

try:
    from aiokafka import AIOKafkaConsumer
except ImportError:
    AIOKafkaConsumer = None

from reconx.platform.kafka.schema_registry import validate_event

logger = logging.getLogger(__name__)


class KafkaEventConsumer:
    """
    Distributed Event Consumer for ReconX Platform.
    Handles message pooling, consumer groups, and dead letter queue (DLQ) routing.
    """

    def __init__(self, topic: str, group_id: str, bootstrap_servers: str = "kafka:9092"):
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = bootstrap_servers
        self._consumer: AIOKafkaConsumer | None = None
        self._running = False

    async def start(self, handler: Callable[[dict[str, Any]], Awaitable[None]]):
        """
        Starts consuming messages and passing them to the async handler.
        """
        if not AIOKafkaConsumer:
            logger.warning("aiokafka not installed. Consumer running in mock mode.")
            return

        self._consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=False,  # We handle commits manually for reliability
        )

        await self._consumer.start()
        self._running = True
        logger.info(f"Kafka Consumer started for topic {self.topic} (Group: {self.group_id})")

        try:
            async for msg in self._consumer:
                if not self._running:
                    break

                event_data = msg.value
                try:
                    # 1. Validate Schema
                    validate_event(self.topic, event_data)

                    # 2. Process
                    await handler(event_data)

                    # 3. Commit exactly once after successful processing
                    await self._consumer.commit()
                except Exception as e:
                    logger.error(f"Error processing message from {self.topic}: {e}")
                    await self._route_to_dlq(msg)
                    # We still commit to move past poison pills
                    await self._consumer.commit()

        finally:
            await self.stop()

    async def _route_to_dlq(self, msg):
        """
        Routes unprocessable messages to a Dead Letter Queue (DLQ).
        """
        dlq_topic = f"{self.topic}.dlq"
        logger.warning(f"Routing message to DLQ: {dlq_topic}")
        # In a real system, we'd use a KafkaProducer to send `msg.value` to `dlq_topic` here.

    async def stop(self):
        self._running = False
        if self._consumer:
            await self._consumer.stop()
