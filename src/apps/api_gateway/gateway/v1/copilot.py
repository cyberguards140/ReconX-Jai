from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from apps.api_gateway.gateway.router_registry import registry
from ai.copilot import copilot_engine

router = APIRouter()
registry.register(router, prefix="/copilot", version="v1", tags=["copilot"])

class ChatRequest(BaseModel):
    query: str
    tenant_id: str = "default_tenant"
    session_id: str = "default_session"

@router.post("/chat")
async def copilot_chat(request: ChatRequest):
    """
    Passes natural language query to the AI Security Copilot.
    """
    try:
        response = await copilot_engine.chat(
            user_input=request.query,
            tenant_id=request.tenant_id,
            session_id=request.session_id
        )
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_copilot_status():
    return {"status": "ok", "service": "copilot"}
