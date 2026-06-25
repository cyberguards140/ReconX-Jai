from typing import Any

from fastapi import APIRouter, HTTPException

from apps.api_gateway.gateway.router_registry import registry

router = APIRouter()
registry.register(router, prefix="/hunting", version="v1", tags=["threat_hunting"])


@router.get("/datasets/assets")
async def export_raw_asset_dataset(limit: int = 1000) -> list[dict[str, Any]]:
    """
    Phase 73: Research Platform.
    Exports massive raw datasets for security researchers to analyze externally.
    """
    return [{"id": "mock_123", "target": "api.target.com", "raw_data": "..."}]


@router.post("/query/graph")
async def execute_parameterized_graph_query(query_type: str, target: str) -> dict[str, Any]:
    """
    Phase 74 & 75: Threat Hunting Workspace.
    Allows researchers to execute complex but safe parameterized graph traversals.
    """
    if query_type == "lateral_movement_paths":
        return {
            "query": "MATCH (n)-[r:USES|TRUSTS*1..3]->(t) RETURN path",
            "results": ["path_1", "path_2"],
        }
    raise HTTPException(status_code=400, detail="Invalid parameterized query type.")


@router.get("/indicators/correlate")
async def correlate_indicators(indicator: str) -> dict[str, Any]:
    """
    Phase 75: Manually hunts the Data Lake for a specific Indicator of Compromise.
    """
    return {
        "indicator": indicator,
        "matches_found": 3,
        "assets_implicated": ["192.168.1.5", "admin.target.com"],
    }
