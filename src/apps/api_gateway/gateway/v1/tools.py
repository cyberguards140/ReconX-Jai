import shutil
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()
registry.register(router, prefix="/tools", version="v1", tags=["tools"])

# Mock schemas and tools for now, dynamically checked
AVAILABLE_TOOLS = [
    {"id": "nmap", "category": "recon", "name": "Nmap Port Scanner", "enabled": True},
    {"id": "subfinder", "category": "recon", "name": "Subfinder", "enabled": True},
    {"id": "naabu", "category": "recon", "name": "Naabu", "enabled": True},
    {"id": "amass", "category": "recon", "name": "Amass", "enabled": True},
    {"id": "masscan", "category": "recon", "name": "Masscan", "enabled": True},
    
    {"id": "httpx", "category": "web", "name": "HTTPX", "enabled": True},
    {"id": "ffuf", "category": "web", "name": "FFUF Fuzzer", "enabled": True},
    {"id": "dirsearch", "category": "web", "name": "Dirsearch", "enabled": True},
    
    {"id": "nuclei", "category": "vuln", "name": "Nuclei", "enabled": True},
    {"id": "sqlmap", "category": "vuln", "name": "SQLMap", "enabled": True},
    {"id": "nikto", "category": "vuln", "name": "Nikto Scanner", "enabled": True},
    
    {"id": "cloud_enum", "category": "cloud", "name": "Cloud Enum", "enabled": True},
    {"id": "scoutsuite", "category": "cloud", "name": "ScoutSuite", "enabled": True},
]

class ToolConfigUpdate(BaseModel):
    config: Dict[str, Any]

@router.get("/")
async def get_tools():
    """Returns list of tools and dynamically detects if they are installed (Stage 8)."""
    tools_out = []
    for t in AVAILABLE_TOOLS:
        t_copy = dict(t)
        # Dynamic detection
        t_copy["installed"] = shutil.which(t["id"]) is not None
        tools_out.append(t_copy)
    return tools_out

@router.get("/{tool_id}/schema")
async def get_tool_schema(tool_id: str):
    return {
        "name": tool_id.capitalize(),
        "arguments": [
            {"flag": "threads", "type": "number", "default": 10},
            {"flag": "verbose", "type": "toggle", "default": False}
        ]
    }

@router.get("/{tool_id}/config")
async def get_tool_config(tool_id: str):
    return {"threads": 10, "verbose": False}

@router.post("/{tool_id}/config")
async def save_tool_config(tool_id: str, data: Dict[str, Any]):
    return {"status": "ok"}

@router.get("/{tool_id}/profiles")
async def get_tool_profiles(tool_id: str):
    return [
        {"name": "Fast Scan", "config": {"threads": 50, "verbose": False}},
        {"name": "Deep Scan", "config": {"threads": 5, "verbose": True}}
    ]

@router.post("/{tool_id}/command")
async def get_tool_command(tool_id: str, data: Dict[str, Any]):
    target = data.get("target", "")
    config = data.get("config", {})
    threads = config.get("threads", 10)
    v = "-v" if config.get("verbose") else ""
    return {"command": f"{tool_id} {v} -t {threads} {target}"}

