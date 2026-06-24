from reconx.database.repositories.base import BaseRepository
from reconx.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

class UserRepository(BaseRepository[User]):
    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        res = await db.execute(select(User).filter(User.username == username))
        return res.scalars().first()

    async def get_by_username_or_email(self, db: AsyncSession, username: str, email: str) -> Optional[User]:
        res = await db.execute(select(User).filter((User.username == username) | (User.email == email)))
        return res.scalars().first()


user_repo = UserRepository(User)
