from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from apps.api_gateway.gateway.router_registry import registry
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
registry.register(router, prefix="/marketplace", version="v1", tags=["marketplace"])

# Mock Database for Marketplace Plugins
MOCK_MARKETPLACE_DB = [
    {"id": "plugin-nuclei-pro", "name": "Nuclei Enterprise Templates", "type": "official", "status": "available"},
    {"id": "plugin-aws-stealer", "name": "AWS IAM Enumerator", "type": "community", "status": "installed"},
    {"id": "plugin-shodan-enterprise", "name": "Shodan Firehose", "type": "official", "status": "available"}
]

@router.get("/plugins")
async def list_plugins() -> List[Dict[str, Any]]:
    """Lists available and installed plugins from the marketplace."""
    return MOCK_MARKETPLACE_DB

@router.post("/plugins/{plugin_id}/install")
async def install_plugin(plugin_id: str):
    """Mocks the installation of a plugin by updating its status."""
    for plugin in MOCK_MARKETPLACE_DB:
        if plugin["id"] == plugin_id:
            if plugin["status"] == "installed":
                raise HTTPException(status_code=400, detail="Plugin already installed")
            
            plugin["status"] = "installed"
            logger.info(f"Installed Marketplace Plugin: {plugin_id}")
            # In reality, we would trigger `git clone` or `pip install` via a background worker here
            return {"status": "success", "message": f"Plugin {plugin_id} installed successfully"}
            
    raise HTTPException(status_code=404, detail="Plugin not found")

@router.post("/plugins/{plugin_id}/disable")
async def disable_plugin(plugin_id: str):
    for plugin in MOCK_MARKETPLACE_DB:
        if plugin["id"] == plugin_id:
            plugin["status"] = "disabled"
            return {"status": "success"}
    raise HTTPException(status_code=404, detail="Plugin not found")
