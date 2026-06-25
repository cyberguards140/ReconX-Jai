from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from data.database.models import Asset

class AssetService:
    @staticmethod
    def create_asset(db: Session, project_id: str, asset_type: str, value: str, tags: list = None, owner_id: str = None) -> Asset:
        asset = Asset(
            project_id=project_id,
            asset_type=asset_type,
            value=value,
            tags=tags or [],
            owner_id=owner_id,
            lifecycle_status="active"
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def get_asset(db: Session, asset_id: str) -> Optional[Asset]:
        return db.get(Asset, asset_id)

    @staticmethod
    def list_assets(db: Session, project_id: str, skip: int = 0, limit: int = 100, search: str = None) -> List[Asset]:
        stmt = select(Asset).where(Asset.project_id == project_id)
        if search:
            stmt = stmt.where(or_(Asset.value.ilike(f"%{search}%"), Asset.asset_type.ilike(f"%{search}%")))
        stmt = stmt.offset(skip).limit(limit)
        return list(db.scalars(stmt))

    @staticmethod
    def update_asset(db: Session, asset_id: str, updates: dict) -> Optional[Asset]:
        asset = db.get(Asset, asset_id)
        if not asset:
            return None
        
        for key, value in updates.items():
            if hasattr(asset, key):
                setattr(asset, key, value)
        
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def delete_asset(db: Session, asset_id: str) -> bool:
        asset = db.get(Asset, asset_id)
        if asset:
            db.delete(asset)
            db.commit()
            return True
        return False
