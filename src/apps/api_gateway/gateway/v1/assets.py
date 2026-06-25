from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from apps.api_gateway.gateway.router_registry import registry
from attack_surface.assets.service import AssetService
from data.database.session import get_db

router = APIRouter()
registry.register(router, prefix="/assets", version="v1", tags=["assets"])


class AssetCreate(BaseModel):
    project_id: str
    asset_type: str
    value: str
    tags: list[str] | None = []
    owner_id: str | None = None


class AssetUpdate(BaseModel):
    tags: list[str] | None = None
    owner_id: str | None = None
    lifecycle_status: str | None = None


@router.post("/", response_model=dict[str, Any])
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    new_asset = AssetService.create_asset(
        db=db,
        project_id=asset.project_id,
        asset_type=asset.asset_type,
        value=asset.value,
        tags=asset.tags,
        owner_id=asset.owner_id,
    )
    return {"status": "success", "asset_id": new_asset.id}


@router.get("/", response_model=dict[str, Any])
def list_assets(
    project_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: str | None = None,
    db: Session = Depends(get_db),
):
    assets = AssetService.list_assets(db, project_id, skip, limit, search)
    return {
        "status": "success",
        "data": [
            {
                "id": a.id,
                "type": a.asset_type,
                "value": a.value,
                "status": a.lifecycle_status,
                "tags": a.tags,
                "owner_id": a.owner_id,
            }
            for a in assets
        ],
    }


@router.get("/{asset_id}", response_model=dict[str, Any])
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = AssetService.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {
        "status": "success",
        "data": {
            "id": asset.id,
            "type": asset.asset_type,
            "value": asset.value,
            "status": asset.lifecycle_status,
            "tags": asset.tags,
            "owner_id": asset.owner_id,
            "created_at": asset.created_at,
        },
    }


@router.put("/{asset_id}", response_model=dict[str, Any])
def update_asset(asset_id: str, updates: AssetUpdate, db: Session = Depends(get_db)):
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    asset = AssetService.update_asset(db, asset_id, update_data)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"status": "success", "message": "Asset updated"}


@router.delete("/{asset_id}", response_model=dict[str, Any])
def delete_asset(asset_id: str, db: Session = Depends(get_db)):
    success = AssetService.delete_asset(db, asset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"status": "success", "message": "Asset deleted"}
