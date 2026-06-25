from fastapi import APIRouter

from apps.api_gateway.gateway.router_registry import registry
from graph.analytics.attack_paths import AttackPathAnalyzer

router = APIRouter()
registry.register(router, prefix="/graph", version="v1", tags=["graph"])


@router.get("/paths/chokepoints")
async def get_chokepoints(project_id: str):
    analyzer = AttackPathAnalyzer()
    chokepoints = await analyzer.identify_chokepoints(project_id)
    return {"status": "success", "data": chokepoints}


@router.get("/paths/blast-radius")
async def get_blast_radius(asset_id: str, depth: int = 3):
    analyzer = AttackPathAnalyzer()
    impacted = await analyzer.map_blast_radius(asset_id, max_depth=depth)
    return {"status": "success", "data": impacted}


@router.get("/")
async def get_graph():
    return {"status": "ok", "service": "graph"}
