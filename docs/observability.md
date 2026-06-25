# Observability & Metrics

ReconX maintains comprehensive insights into the active health, system throughput, and workflow execution states using a centralized observability layer.

## Health Probes

Two primary endpoints are available under `src/reconx/observability/health.py`:

- `GET /health/health`: Simple Liveness probe (`{"status": "healthy"}`).
- `GET /health/status`: Detailed Readiness probe inspecting the Database and EventBus connectivity.

## Prometheus Metrics

The `MetricsRegistry` captures throughput directly from the `EventBus` hooks.

- `GET /metrics`: Emits a standard `CONTENT_TYPE_LATEST` payload of counters (e.g., `WorkflowCompleted`, `TaskFailed`) suitable for Prometheus scraping and Grafana dashboard visualization.

## Tracing and Correlation

A `correlation_id` automatically traces the entire lifecycle of a workflow execution. The engine generates this ID initially and bubbles it down to the `TaskExecutor`. 

The `LoggingHandler` seamlessly unpacks this correlation ID into the log output to allow robust queries within logging aggregation platforms.