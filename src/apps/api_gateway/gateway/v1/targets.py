from fastapi import APIRouter
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()

# Register the router
registry.register(router, prefix="/targets", version="v1", tags=["targets"])

@router.get("/")
async def get_targets():
    return {"status": "ok", "service": "targets"}
