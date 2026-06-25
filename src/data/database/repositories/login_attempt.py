from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.database.models import LoginAttempt
from data.database.repositories.base import BaseRepository


class LoginAttemptRepository(BaseRepository[LoginAttempt]):
    async def get_recent_failures(
        self, db: AsyncSession, username: str, since: datetime
    ) -> list[LoginAttempt]:
        res = await db.execute(
            select(LoginAttempt).filter(
                LoginAttempt.username == username,
                LoginAttempt.successful.is_(False),
                LoginAttempt.timestamp >= since,
            )
        )
        return list(res.scalars().all())


login_attempt_repo = LoginAttemptRepository(LoginAttempt)
