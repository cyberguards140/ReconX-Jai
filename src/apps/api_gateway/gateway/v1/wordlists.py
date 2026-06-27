import os
from fastapi import APIRouter
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()
registry.register(router, prefix="/wordlists", version="v1", tags=["wordlists"])

@router.get("/")
async def get_wordlists():
    """Returns available wordlists (simulated from disk)."""
    return [
        {"id": "default", "name": "Default Small (10k)", "size": "1.2MB"},
        {"id": "medium", "name": "Medium List (50k)", "size": "5.4MB"},
        {"id": "large", "name": "AssetNote Large (2M)", "size": "150MB"},
        {"id": "custom", "name": "Custom Uploads", "size": "Various"}
    ]
