from fastapi import APIRouter

from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()

# Register the router
registry.register(router, prefix="/auth", version="v1", tags=["auth"])


@router.get("/")
async def get_auth():
    return {"status": "ok", "service": "auth"}
