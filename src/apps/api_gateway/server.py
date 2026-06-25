"""ReconX API server launcher."""

import uvicorn
from fastapi import FastAPI
from apps.api_gateway.gateway.router_registry import registry
from apps.api_gateway.gateway.routes import analytics, asm, cloud, events, executive, external, infra, soc, threat, visual
from apps.api_gateway.gateway.v1 import auth, projects, targets, assets, scans, findings, reports, workflows, intelligence, graph
from apps.api_gateway.gateway.v1 import analytics as v1_analytics

from contextlib import asynccontextmanager
from core.scheduler.monitoring_engine import monitoring_engine
from recon.services.pipeline_engine import pipeline_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Events
    pipeline_engine.start()
    monitoring_engine.start()
    yield
    # Shutdown Events
    await monitoring_engine.stop()
    await pipeline_engine.stop()

app = FastAPI(
    title="ReconX X - Enterprise Intelligence Engine",
    description="""
    The world's most advanced autonomous attack surface management and intelligence platform.
    
    ## Core Features:
    * **Autonomous Swarm**: AI-driven discovery loops.
    * **Digital Twin**: Neo4j Graph analysis of breach paths.
    * **Global Scale**: Multi-regional Kafka dispatching.
    """,
    version="X.0.0-ULTIMATE",
    contact={
        "name": "ReconX Security Engineering",
        "url": "https://reconx.io/support",
        "email": "security@reconx.io",
    },
    license_info={
        "name": "Enterprise Commercial License",
    },
    lifespan=lifespan
)

from fastapi.responses import FileResponse
import os

for router, prefix, version, tags in registry.get_routers():
    app.include_router(router, prefix=f"/api/{version}{prefix}", tags=tags)

@app.get("/dashboard", tags=["ui"])
async def serve_dashboard():
    """Serves the main ReconX Dashboard UI."""
    dashboard_path = os.path.join(os.path.dirname(__file__), "..", "dashboard", "frontend", "reconx-dashboard-v2.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"error": "Dashboard UI not found"}


def start_server(port: int = 8000) -> None:
    """Start the ReconX API server."""
    uvicorn.run(
        "reconx.api.server:app",
        host="0.0.0.0",  # noqa: S104
        port=port,
        reload=False,
    )
