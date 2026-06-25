import json
import logging
from typing import Any

try:
    from aiokafka import AIOKafkaProducer
except ImportError:
    AIOKafkaProducer = None

from reconx.platform.kafka.schema_registry import validate_event

logger = logging.getLogger(__name__)


class KafkaEventProducer:
    """
    Distributed Event Producer for ReconX Platform.
    Handles at-least-once delivery, retry logic, and schema validation.
    """

    def __init__(self, bootstrap_servers: str = "kafka:9092"):
        self.bootstrap_servers = bootstrap_servers
        self._producer: AIOKafkaProducer | None = None

    async def start(self):
        if not AIOKafkaProducer:
            logger.warning("aiokafka not installed. Kafka Event Producer running in mock mode.")
            return

        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5,
            acks="all",  # Wait for all replicas to acknowledge for durability
        )
        await self._producer.start()
        logger.info(f"Kafka Producer connected to {self.bootstrap_servers}")

    async def stop(self):
        if self._producer:
            await self._producer.stop()

    async def publish(self, topic: str, event_data: dict[str, Any], key: str | None = None):
        """
        Publishes an event to a Kafka topic after validating its schema.
        """
        # 1. Schema Validation
        validate_event(topic, event_data)

        # 2. Publish
        if not self._producer:
            logger.debug(f"[MOCK KAFKA] Publishing to {topic}: {event_data}")
            return

        try:
            b_key = key.encode("utf-8") if key else None
            await self._producer.send_and_wait(topic, value=event_data, key=b_key)
        except Exception as e:
            logger.error(f"Failed to publish event to topic {topic}: {e}")
            raise
