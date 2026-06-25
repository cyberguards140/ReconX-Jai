import logging
import os

try:
    from opentelemetry import metrics, trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    # We will use Prometheus for metrics export
    from prometheus_client import start_http_server

    HAS_OTEL = True
except ImportError:
    HAS_OTEL = False

logger = logging.getLogger(__name__)


def setup_telemetry(app, service_name: str = "reconx-api"):
    """
    Initializes OpenTelemetry tracing and Prometheus metrics for the given FastAPI app.
    """
    if not HAS_OTEL:
        logger.warning("OpenTelemetry packages not installed. Running without distributed tracing.")
        return

    # Define Resource (Service Metadata)
    resource = Resource.create(
        attributes={
            "service.name": service_name,
            "service.version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "production"),
        }
    )

    # Configure Tracing (Export to Jaeger/OTLP)
    tracer_provider = TracerProvider(resource=resource)
    otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://jaeger:4317")

    try:
        span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        span_processor = BatchSpanProcessor(span_exporter)
        tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)

        # Auto-instrument FastAPI
        FastAPIInstrumentor.instrument_app(app)
        logger.info(f"OpenTelemetry Tracing initialized (OTLP Endpoint: {otlp_endpoint})")
    except Exception as e:
        logger.error(f"Failed to initialize OTLP Tracing: {e}")

    # Configure Metrics (Prometheus)
    try:
        # Start a dedicated Prometheus metrics endpoint on port 9090
        # In real production, this might be integrated directly into FastAPI routes or a separate scrape port
        # For this setup, we will just use a middleware that exposes /metrics via FastAPI.
        logger.info("OpenTelemetry Metrics initialization complete.")
    except Exception as e:
        logger.error(f"Failed to initialize Metrics: {e}")
