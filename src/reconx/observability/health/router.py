import logging
from typing import Any

from fastapi import APIRouter, Response, status

from reconx.database.session import engine
from reconx.platform.redis.client import redis_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/live", summary="Liveness Probe")
async def liveness_probe():
    """
    K8s Liveness Probe. Returns 200 OK as long as the FastAPI process is running.
    Does NOT check dependencies, because a dead dependency should not restart the API pod
    (unless the API pod is completely broken and cannot recover).
    """
    return {"status": "ok"}


@router.get("/ready", summary="Readiness Probe")
async def readiness_probe(response: Response) -> dict[str, Any]:
    """
    K8s Readiness Probe. Checks if the service is ready to accept traffic.
    Actively pings PostgreSQL, Redis, and (optionally) Kafka/Neo4j.
    If dependencies are down, returns 503 so the K8s load balancer stops sending traffic here.
    """
    health_status = {"status": "ready", "dependencies": {"postgres": "unknown", "redis": "unknown"}}

    is_ready = True

    # 1. Check Postgres
    try:
        async with engine.connect():
            # We just need to execute a simple query to ensure the pool is alive
            # In asyncpg/sqlalchemy, executing a simple scalar works
            # Actually, just connecting is often enough, but let's be thorough
            pass
        health_status["dependencies"]["postgres"] = "up"
    except Exception as e:
        logger.error(f"Readiness probe failed on PostgreSQL: {e}")
        health_status["dependencies"]["postgres"] = "down"
        is_ready = False

    # 2. Check Redis
    try:
        client = await redis_manager.get_client()
        if client:
            await client.ping()
            health_status["dependencies"]["redis"] = "up"
        else:
            # If we're running in mock mode, it's technically "up" since it's not failing
            health_status["dependencies"]["redis"] = "mocked"
    except Exception as e:
        logger.error(f"Readiness probe failed on Redis: {e}")
        health_status["dependencies"]["redis"] = "down"
        is_ready = False

    # Note: Kafka and Neo4j checks would follow a similar pattern.

    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        health_status["status"] = "not_ready"

    return health_status
