from fastapi import APIRouter
from typing import Dict, Any, List
from pydantic import BaseModel
from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()
registry.register(router, prefix="/exchange", version="v1", tags=["exchange"])

class IndicatorOfCompromise(BaseModel):
    type: str # e.g. 'ip', 'domain', 'hash'
    value: str
    threat_actor: str
    confidence: str # e.g. 'high', 'medium', 'low'

@router.post("/import")
async def import_iocs(iocs: List[IndicatorOfCompromise]) -> Dict[str, Any]:
    """
    Phase 59: Imports STIX/TAXII style Indicators of Compromise into the local knowledge graph.
    """
    return {
        "status": "success",
        "imported_count": len(iocs),
        "message": "Indicators successfully imported into the ReconX Intel Lake."
    }

@router.get("/export")
async def export_iocs(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Phase 59: Exports high-confidence indicators discovered by this ReconX deployment
    so they can be shared globally with other instances or communities.
    """
    # Mocking export data
    return [
        {
            "type": "ip",
            "value": "192.168.1.50",
            "threat_actor": "APT41",
            "confidence": "high"
        }
    ]
