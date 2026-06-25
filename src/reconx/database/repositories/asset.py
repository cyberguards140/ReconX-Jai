from reconx.database.repositories.base import BaseRepository
from reconx.database.models import Asset, AssetHistory, AssetRelationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

class AssetRepository(BaseRepository[Asset]):
    async def get_by_value(self, db: AsyncSession, project_id: str, asset_type: str, value: str) -> Optional[Asset]:
        res = await db.execute(
            select(Asset).filter(
                Asset.project_id == project_id,
                Asset.asset_type == asset_type,
                Asset.value == value,
            )
        )
        return res.scalars().first()

class AssetHistoryRepository(BaseRepository[AssetHistory]):
    pass

class AssetRelationshipRepository(BaseRepository[AssetRelationship]):
    async def get_relationship(self, db: AsyncSession, p_id: str, c_id: str) -> Optional[AssetRelationship]:
        res = await db.execute(
            select(AssetRelationship).filter(
                AssetRelationship.parent_asset_id == p_id,
                AssetRelationship.child_asset_id == c_id,
            )
        )
        return res.scalars().first()

asset_repo = AssetRepository(Asset)
asset_history_repo = AssetHistoryRepository(AssetHistory)
asset_rel_repo = AssetRelationshipRepository(AssetRelationship)
