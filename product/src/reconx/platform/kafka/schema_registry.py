import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Basic Event Schemas for Platform
SCHEMAS = {
    "assets.events": {
        "required_fields": ["event_type", "asset_id", "timestamp"]
    },
    "threat.events": {
        "required_fields": ["event_type", "indicator", "severity", "timestamp"]
    },
    "workflow.events": {
        "required_fields": ["event_type", "workflow_id", "status", "timestamp"]
    }
}

class SchemaValidationError(Exception):
    pass

def validate_event(topic: str, event_data: Dict[str, Any]):
    """
    Validates that the outgoing/incoming event matches the registered schema for the topic.
    In a fully decoupled system, this might use Confluent Schema Registry with Avro/Protobuf.
    """
    schema = SCHEMAS.get(topic)
    if not schema:
        # If no strict schema is registered, allow by default but warn.
        logger.debug(f"No schema registered for topic: {topic}")
        return

    missing_fields = [f for f in schema["required_fields"] if f not in event_data]
    if missing_fields:
        raise SchemaValidationError(
            f"Event for topic {topic} is missing required fields: {missing_fields}"
        )
