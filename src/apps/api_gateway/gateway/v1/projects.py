from fastapi import APIRouter

from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()

# Register the router
registry.register(router, prefix="/projects", version="v1", tags=["projects"])


@router.get("/")
async def get_projects():
    return {"status": "ok", "service": "projects"}
