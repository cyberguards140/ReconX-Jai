from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api_gateway.gateway.router_registry import registry
from attack_surface.assets.analytics import AnalyticsEngine
from data.database.session import get_db

router = APIRouter()
registry.register(router, prefix="/analytics", version="v1", tags=["analytics"])


@router.get("/attack-surface", response_model=dict[str, Any])
def get_attack_surface_overview(project_id: str = "default", db: Session = Depends(get_db)):
    overview = AnalyticsEngine.get_attack_surface_overview(db, project_id)
    trends = AnalyticsEngine.get_risk_trends(db, project_id)

    return {"status": "success", "data": {"inventory": overview, "trends": trends}}
