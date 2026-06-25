from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api_gateway.gateway.router_registry import registry
from data.database.session import get_db
from data.timeline_engine import timeline_engine

router = APIRouter()
registry.register(router, prefix="/timeline", version="v1", tags=["timeline"])


@router.get("/{asset_id}")
async def get_asset_timeline(asset_id: str, db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    """
    Retrieves the complete historical lifecycle timeline for a specific asset.
    """
    history = timeline_engine.get_timeline(db, asset_id)
    return history
