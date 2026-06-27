from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai.engine import ai_engine
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()
registry.register(router, prefix="/intelligence", version="v1", tags=["intelligence"])


class SynthesizeRequest(BaseModel):
    finding_data: dict[str, Any]


@router.post("/synthesize")
async def synthesize_finding(request: SynthesizeRequest):
    """
    Passes finding data to the LLM engine for executive-level remediation strategy.
    """
    try:
        report = await ai_engine.synthesize_finding(request.finding_data)
        return {"status": "success", "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_intelligence():
    return {"status": "ok", "service": "intelligence"}

@router.get("/exposure")
async def get_exposure():
    """Returns general exposure analytics."""
    return {
        "status": "ok",
        "exposure_score": 75,
        "critical_risks": 2,
        "high_risks": 5
    }

@router.get("/threat")
async def get_threat_intel():
    """Returns threat intelligence indicators."""
    return {
        "status": "ok",
        "active_campaigns": 1,
        "ioc_matches": 3
    }
