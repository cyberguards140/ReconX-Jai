from reconx.database.repositories.base import BaseRepository
from reconx.database.models import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    async def get_by_token_id(self, db: AsyncSession, token_id: str) -> Optional[RefreshToken]:
        res = await db.execute(select(RefreshToken).filter(RefreshToken.token_id == token_id))
        return res.scalars().first()


refresh_token_repo = RefreshTokenRepository(RefreshToken)
