from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.database.models import RefreshToken
from data.database.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    async def get_by_token_id(self, db: AsyncSession, token_id: str) -> RefreshToken | None:
        res = await db.execute(select(RefreshToken).filter(RefreshToken.token_id == token_id))
        return res.scalars().first()


refresh_token_repo = RefreshTokenRepository(RefreshToken)
