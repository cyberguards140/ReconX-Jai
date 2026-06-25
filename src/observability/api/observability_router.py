from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter(tags=["Observability"])


@router.get("/metrics", response_class=PlainTextResponse, summary="Prometheus Scrape Endpoint")
async def metrics():
    """
    Exposes application metrics for Prometheus scraping.
    Note: In highly secure environments, this endpoint should be restricted to internal network traffic only,
    or protected via specific Prometheus bearer tokens.
    """
    data = generate_latest()
    return PlainTextResponse(content=data, media_type=CONTENT_TYPE_LATEST)


# Note: Additional telemetry summary APIs (e.g., getting SLIs directly for the dashboard)
# could be added here if the dashboard doesn't query Grafana/Prometheus directly.
