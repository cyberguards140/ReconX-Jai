from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from reconx.auth.middleware import SecurityMiddleware
from reconx.data_fabric.analytics.engine import analytics_engine
from reconx.data_fabric.catalog.registry import metadata_catalog
from reconx.data_fabric.lineage.tracker import lineage_tracker
from reconx.data_fabric.query_engine.federated import federated_engine
from reconx.enterprise.isolation.tenant_context import get_current_tenant_id

router = APIRouter(tags=["Data Fabric"], dependencies=[Depends(SecurityMiddleware)])


class QueryRequest(BaseModel):
    query_string: str
    parameters: dict[str, Any] = None


@router.get("/catalog", summary="Get Metadata Catalog")
async def get_catalog():
    return {"catalog": metadata_catalog.get_catalog()}


@router.get("/lineage/{target_id}", summary="Get Data Lineage")
async def get_lineage(target_id: str):
    return {"lineage": lineage_tracker.get_lineage(target_id)}


@router.post("/query", summary="Execute Federated Query")
async def execute_query(request: QueryRequest):
    """
    Query the Lakehouse, Neo4j, or Postgres using a single interface.
    """
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant context missing"
        )

    return federated_engine.execute_query(request.query_string, request.parameters)


@router.get("/analytics/risk-velocity", summary="Get Risk Velocity Analytics")
async def get_risk_velocity():
    return analytics_engine.calculate_risk_velocity()
