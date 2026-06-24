from reconx.database.repositories.base import BaseRepository
from reconx.database.models import LoginAttempt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

class LoginAttemptRepository(BaseRepository[LoginAttempt]):
    async def get_recent_failures(self, db: AsyncSession, username: str, since: datetime) -> List[LoginAttempt]:
        res = await db.execute(
            select(LoginAttempt).filter(
                LoginAttempt.username == username,
                LoginAttempt.successful.is_(False),
                LoginAttempt.timestamp >= since,
            )
        )
        return list(res.scalars().all())


login_attempt_repo = LoginAttemptRepository(LoginAttempt)
