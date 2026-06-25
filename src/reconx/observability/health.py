from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from reconx.database.session import get_db
from sqlalchemy import text
from reconx.events.bus import event_bus
from reconx.config.settings import settings
import os

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/health")
async def liveness():
    return {"status": "healthy"}

@router.get("/status")
async def readiness(db: AsyncSession = Depends(get_db)):
    status = {"database": "disconnected", "event_bus": "disconnected"}
    
    # Check Database
    try:
        await db.execute(text("SELECT 1"))
        status["database"] = "connected"
    except Exception:
        pass

    # Check Event Bus
    try:
        if len(event_bus.subscribers) > 0:
            status["event_bus"] = "connected"
    except Exception:
        pass
        
    healthy = status["database"] == "connected"
    return {"status": "ready" if healthy else "not_ready", "components": status}

@router.get("/ready")
async def readiness_probe(db: AsyncSession = Depends(get_db)):
    """Kubernetes-style readiness probe combining settings validation and backend checks."""
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        return {"ready": False, "reason": "Database unreachable"}
        
    if not os.path.exists(settings.workflow_directory):
        return {"ready": False, "reason": f"Workflow directory '{settings.workflow_directory}' missing"}
        
    return {"ready": True, "environment": settings.app_env}
