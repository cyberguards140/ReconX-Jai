from fastapi import APIRouter, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import uuid
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from apps.api_gateway.gateway.router_registry import registry
from data.database.repositories.scan import scan_repo
from data.database.models import Scan
from data.database.session import get_db
from core.messaging.broker import broker

router = APIRouter()
registry.register(router, prefix="/jobs", version="v1", tags=["jobs"])

class JobRequest(BaseModel):
    tool_id: str
    target: str
    config: Optional[Dict[str, Any]] = None

@router.post("/create")
async def create_job(req: JobRequest, db: AsyncSession = Depends(get_db)):
    job_id = str(uuid.uuid4())
    await scan_repo.create(db, obj_in={
        "id": job_id,
        "scan_type": req.tool_id,
        "target_id": req.target,
        "project_id": "default",
        "status": "pending",
        "started_at": datetime.datetime.utcnow()
    })
    return {"status": "ok", "job_id": job_id}

@router.get("/running")
async def get_running_jobs(db: AsyncSession = Depends(get_db)):
    scans = await scan_repo.get_multi(db)
    running = [s for s in scans if s.status == "pending" or s.status == "running"]
    out = []
    for s in running:
        out.append({
            "id": s.id,
            "tool_id": s.scan_type,
            "target": s.target_id,
            "status": s.status
        })
    return out

@router.post("/{job_id}/stop")
async def stop_job(job_id: str, db: AsyncSession = Depends(get_db)):
    job = await scan_repo.get(db, job_id)
    if job:
        await scan_repo.update(db, db_obj=job, obj_in={"status": "stopped", "finished_at": datetime.datetime.utcnow()})
        
    asyncio.create_task(broker.publish("ws_broadcast", {
        "type": "job_status", 
        "tool_id": "all",
        "status": "stopped"
    }))
    return {"status": "ok"}

@router.post("/{job_id}/pause")
async def pause_job(job_id: str, db: AsyncSession = Depends(get_db)):
    job = await scan_repo.get(db, job_id)
    if job:
        await scan_repo.update(db, db_obj=job, obj_in={"status": "paused"})
        
    asyncio.create_task(broker.publish("ws_broadcast", {
        "type": "job_status", 
        "tool_id": "all",
        "status": "paused"
    }))
    return {"status": "ok"}
