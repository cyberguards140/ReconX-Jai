"""ReconX API server launcher."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from apps.api_gateway.gateway.router_registry import registry
from core.scheduler.monitoring_engine import monitoring_engine
from recon.services.pipeline_engine import pipeline_engine


from data.database.session import engine
from data.database.base import BaseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Events
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
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
    lifespan=lifespan,
)

import os

from fastapi.responses import FileResponse

import importlib
import pkgutil
import apps.api_gateway.gateway.v1 as gateway_v1

# Dynamically import all modules in gateway.v1 to trigger registry.register
for _, module_name, _ in pkgutil.iter_modules(gateway_v1.__path__):
    importlib.import_module(f"apps.api_gateway.gateway.v1.{module_name}")

for router, prefix, version, tags in registry.get_routers():
    app.include_router(router, prefix=f"/api/{version}{prefix}", tags=tags)

from fastapi.staticfiles import StaticFiles
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dashboard", "frontend"))
app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")


from fastapi.responses import FileResponse, RedirectResponse

@app.get("/", tags=["ui"], include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard", tags=["ui"])
async def serve_dashboard():
    """Serves the main ReconX Dashboard UI."""
    dashboard_path = os.path.join(frontend_dir, "reconx-dashboard-v2.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"error": "Dashboard UI not found"}


def start_server(port: int = 8000) -> None:
    """Start the ReconX API server."""
    uvicorn.run(
        "apps.api_gateway.server:app",
        host="0.0.0.0",  # noqa: S104
        port=port,
        reload=False,
    )
