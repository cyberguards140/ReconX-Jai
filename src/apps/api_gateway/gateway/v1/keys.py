from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()
registry.register(router, prefix="/keys", version="v1", tags=["keys"])

class KeyUpdateRequest(BaseModel):
    keys: Dict[str, str]

# In-memory storage for MVP. In prod, this goes to HashiCorp Vault or encrypted DB.
STORED_KEYS = {
    "shodan": "",
    "github": "",
    "censys": "",
    "virustotal": ""
}

@router.get("/")
async def get_keys():
    """Returns stored API keys (obfuscated)."""
    obfuscated = {}
    for k, v in STORED_KEYS.items():
        if v:
            obfuscated[k] = v[:4] + "*" * 10 if len(v) > 4 else "***"
        else:
            obfuscated[k] = ""
    return obfuscated

@router.post("/")
async def save_keys(req: KeyUpdateRequest):
    """Saves API keys to secure storage."""
    for k, v in req.keys.items():
        if v and not v.startswith("*"): # Don't save obfuscated strings back
            STORED_KEYS[k] = v
    return {"status": "ok"}
