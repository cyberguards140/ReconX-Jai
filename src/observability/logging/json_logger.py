import json
import logging
import sys
from datetime import datetime, timezone

try:
    from opentelemetry import trace

    HAS_OTEL = True
except ImportError:
    HAS_OTEL = False

from plugins.enterprise.isolation.tenant_context import get_current_tenant_id


class JSONLogFormatter(logging.Formatter):
    """
    Structured JSON logger for ELK/OpenSearch ingestion.
    Automatically injects OTLP trace context and active tenant boundaries.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "logger": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno,
            "tenant_id": get_current_tenant_id() or "system",
        }

        # Inject OpenTelemetry Trace IDs if available
        if HAS_OTEL:
            span = trace.get_current_span()
            if span and span.is_recording():
                ctx = span.get_span_context()
                if ctx.is_valid:
                    log_entry["trace_id"] = f"{ctx.trace_id:032x}"
                    log_entry["span_id"] = f"{ctx.span_id:016x}"

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def setup_json_logging(log_level=logging.INFO):
    """
    Replaces the default root logger with the JSON format for structured ingestion.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONLogFormatter())
    root_logger.addHandler(handler)

    # Example to quiet down chatty libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
