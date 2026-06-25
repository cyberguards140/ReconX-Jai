from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from core.observability.metrics import metrics_registry
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()
# Metrics are typically exposed at the root level for Prometheus, but we'll register it under /api/v1/metrics for consistency
registry.register(router, prefix="/metrics", version="v1", tags=["observability"])

@router.get("/", response_class=PlainTextResponse)
async def get_prometheus_metrics():
    """
    Endpoint for Prometheus to scrape RED metrics.
    """
    return metrics_registry.generate_prometheus_payload()
