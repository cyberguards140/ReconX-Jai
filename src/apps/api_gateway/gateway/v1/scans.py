from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from apps.api_gateway.gateway.router_registry import registry
from recon.services.pipeline_engine import pipeline_engine

router = APIRouter()
registry.register(router, prefix="/scans", version="v1", tags=["scans"])

class PipelineRequest(BaseModel):
    target: str

@router.post("/pipeline/start")
async def start_pipeline(req: PipelineRequest):
    if not pipeline_engine.running:
        pipeline_engine.start()
    
    # Enqueue into the first stage of the pipeline (subfinder)
    await pipeline_engine.enqueue("subfinder", {"target": req.target, "source": "API"})
    return {"status": "success", "message": f"Pipeline started for {req.target}"}

@router.post("/pipeline/stop")
async def stop_pipeline():
    if pipeline_engine.running:
        await pipeline_engine.stop()
        return {"status": "success", "message": "Pipeline stopping..."}
    return {"status": "error", "message": "Pipeline is not running"}

@router.get("/")
async def get_scans():
    return {"status": "ok", "service": "scans"}
