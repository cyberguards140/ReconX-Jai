from fastapi import APIRouter
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()

# Register the router
registry.register(router, prefix="/findings", version="v1", tags=["findings"])

@router.get("/")
async def get_findings():
    return {"status": "ok", "service": "findings"}
