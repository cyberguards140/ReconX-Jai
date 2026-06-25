import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from reconx.ai.copilot import copilot_engine
from reconx.auth.middleware import SecurityMiddleware
from reconx.enterprise.isolation.tenant_context import get_current_tenant_id

router = APIRouter(tags=["AI Copilot"], dependencies=[Depends(SecurityMiddleware)])


class ChatRequest(BaseModel):
    message: str
    session_id: str = None


class ChatResponse(BaseModel):
    response: str
    explainability: dict[str, Any]


@router.post("/chat", response_model=ChatResponse, summary="Query the AI Security Copilot")
async def chat(request: ChatRequest):
    """
    Submits a natural language query to the AI Security Copilot.
    """
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant context missing"
        )

    session_id = request.session_id or str(uuid.uuid4())

    # Process through Copilot
    result = await copilot_engine.chat(request.message, tenant_id, session_id)

    return ChatResponse(
        response=result["response"], explainability=result.get("explainability", {})
    )


# Note: /investigate, /analyze, /report endpoints would be similar wrappers around
# specific Orchestrator Intents.
