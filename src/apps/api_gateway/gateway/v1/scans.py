from fastapi import APIRouter, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import uuid
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api_gateway.gateway.router_registry import registry
from data.database.repositories.scan import scan_repo
from data.database.models import Scan
from recon.services.pipeline_engine import pipeline_engine
from data.database.session import get_db

router = APIRouter()
registry.register(router, prefix="/scans", version="v1", tags=["scans"])

class PipelineRequest(BaseModel):
    target: str
    wordlist: str = ""
    api_keys: Optional[Dict[str, str]] = None

@router.post("/pipeline/start")
async def start_pipeline(req: PipelineRequest, db: AsyncSession = Depends(get_db)):
    scan_id = str(uuid.uuid4())
    await scan_repo.create(db, obj_in={
        "id": scan_id,
        "scan_type": "Full Pipeline",
        "target_id": req.target,
        "project_id": "default",
        "status": "pending",
        "started_at": datetime.datetime.utcnow()
    })
    
    if not pipeline_engine.running:
        pipeline_engine.start()

    # Enqueue into the first stage of the pipeline
    await pipeline_engine.enqueue("subfinder", {"target": req.target, "source": "API", "scan_id": scan_id})
    return {"status": "ok", "message": "Pipeline started", "scan_id": scan_id}

@router.post("/pipeline/stop")
async def stop_pipeline():
    await pipeline_engine.stop()
    return {"status": "ok", "message": "Pipeline stopped"}

@router.get("/")
async def get_scans(db: AsyncSession = Depends(get_db)):
    scans = await scan_repo.get_multi(db)
    out = []
    for s in scans:
        out.append({
            "id": s.id,
            "target_id": s.target_id,
            "scan_type": s.scan_type,
            "status": s.status,
            "started_at": str(s.started_at) if s.started_at else None
        })
    return out
