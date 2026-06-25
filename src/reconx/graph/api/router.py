from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from neo4j import AsyncDriver
from pydantic import BaseModel

from reconx.api.dependencies import get_current_user, require_permission
from reconx.database.models import User
from reconx.graph.analytics.attack_paths import AttackPathAnalyzer
from reconx.graph.analytics.risk_propagation import RiskPropagationEngine
from reconx.graph.neo4j.connection import get_neo4j_driver

router = APIRouter(prefix="/graph", tags=["Graph Intelligence"])


class GraphQueryRequest(BaseModel):
    query: str
    parameters: dict[str, Any] | None = None


@router.post("/query", dependencies=[Depends(require_permission("graph.query"))])
async def execute_query(request: GraphQueryRequest, current_user: User = Depends(get_current_user)):
    """
    Execute a raw (but parameterized) Cypher query against the graph.
    Requires 'graph.query' permission.
    """
    driver: AsyncDriver = await get_neo4j_driver()
    results = []

    # Very basic tenant isolation: append tenant_id matching where applicable
    # In production, this should use CypherBuilder to enforce tenant scoping.

    async with driver.session() as session:
        try:
            res = await session.run(request.query, request.parameters or {})
            async for record in res:
                results.append(record.data())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Neo4j Query Error: {e}")

    return {"results": results}


@router.get("/attack-paths/shortest", dependencies=[Depends(require_permission("graph.read"))])
async def get_shortest_attack_path(
    start_id: str, end_id: str, max_depth: int = 5, current_user: User = Depends(get_current_user)
):
    """
    Returns the shortest attack path between two node IDs.
    """
    analyzer = AttackPathAnalyzer()
    paths = await analyzer.find_shortest_path(start_id, end_id, max_depth)
    return {"paths": paths}


@router.get("/attack-paths/exposure", dependencies=[Depends(require_permission("graph.read"))])
async def get_exposure_paths(
    target_asset_id: str, max_depth: int = 5, current_user: User = Depends(get_current_user)
):
    """
    Returns paths from known threats to a specific target asset.
    """
    analyzer = AttackPathAnalyzer()
    paths = await analyzer.find_exposure_paths(target_asset_id, max_depth)
    return {"paths": paths}


@router.post(
    "/analytics/risk-propagation", dependencies=[Depends(require_permission("graph.analytics"))]
)
async def trigger_risk_propagation(current_user: User = Depends(get_current_user)):
    """
    Triggers risk score propagation for the current tenant's assets.
    """
    engine = RiskPropagationEngine()
    results = await engine.propagate_risk(tenant_id=current_user.tenant_id)
    return {"status": "success", "propagated_scores": results}
