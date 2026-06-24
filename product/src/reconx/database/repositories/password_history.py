from reconx.database.repositories.base import BaseRepository
from reconx.database.models import PasswordHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class PasswordHistoryRepository(BaseRepository[PasswordHistory]):
    async def get_recent_history(self, db: AsyncSession, user_id: str, limit: int) -> List[PasswordHistory]:
        res = await db.execute(
            select(PasswordHistory)
            .filter(PasswordHistory.user_id == user_id)
            .order_by(PasswordHistory.created_at.desc())
            .limit(limit)
        )
        return list(res.scalars().all())


password_history_repo = PasswordHistoryRepository(PasswordHistory)
