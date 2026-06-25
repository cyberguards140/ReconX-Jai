from fastapi import APIRouter
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()

# Register the router
registry.register(router, prefix="/workflows", version="v1", tags=["workflows"])

@router.get("/")
async def get_workflows():
    return {"status": "ok", "service": "workflows"}
