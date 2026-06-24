from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List

from reconx.enterprise.isolation.tenant_context import get_current_tenant_id
from reconx.auth.middleware import SecurityMiddleware

from reconx.command_center.secos_core.state import secos_state
from reconx.command_center.command_bus.router import command_bus
from reconx.command_center.coordination.timeline import global_timeline
from reconx.command_center.decisions.center import decision_center
from reconx.command_center.governance.mission_control import mission_control

router = APIRouter(tags=["Cyber Defense Command Center"], dependencies=[Depends(SecurityMiddleware)])

class CommandRequest(BaseModel):
    command_name: str
    payload: Dict[str, Any]

@router.get("/overview", summary="Get SecOS Global State")
async def get_overview():
    """
    Retrieves the macro-level health, active incidents, and operations state.
    """
    if not get_current_tenant_id():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant context missing")
        
    return secos_state.get_global_state()

@router.get("/timeline", summary="Get Global Security Timeline")
async def get_timeline(limit: int = 50):
    """
    Retrieves chronological cross-domain events.
    """
    return {"timeline": global_timeline.query_timeline(limit=limit)}

@router.get("/decisions", summary="Get Pending Decisions")
async def get_decisions():
    """
    Retrieves all autonomous actions requiring HITL approval.
    """
    return {"pending_decisions": decision_center.get_pending_decisions()}

@router.get("/missions", summary="Get Mission Control Metrics")
async def get_missions():
    """
    Retrieves operational metrics and ROI tracking.
    """
    return {"metrics": mission_control.get_mission_metrics()}

@router.post("/command", summary="Dispatch a Command via the Command Bus")
async def dispatch_command(request: CommandRequest):
    """
    A single routing endpoint for triggering workflows, AI Copilot, or Triage.
    """
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant context missing")
        
    global_timeline.log_event(
        event_type="command_dispatched",
        source="api",
        payload={"command": request.command_name}
    )
        
    return command_bus.dispatch(request.command_name, request.payload)
