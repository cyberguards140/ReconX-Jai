from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.database.models import PasswordHistory
from data.database.repositories.base import BaseRepository


class PasswordHistoryRepository(BaseRepository[PasswordHistory]):
    async def get_recent_history(
        self, db: AsyncSession, user_id: str, limit: int
    ) -> list[PasswordHistory]:
        res = await db.execute(
            select(PasswordHistory)
            .filter(PasswordHistory.user_id == user_id)
            .order_by(PasswordHistory.created_at.desc())
            .limit(limit)
        )
        return list(res.scalars().all())


password_history_repo = PasswordHistoryRepository(PasswordHistory)
