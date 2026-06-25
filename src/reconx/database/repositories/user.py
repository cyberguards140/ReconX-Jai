from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from reconx.database.models import User
from reconx.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        res = await db.execute(select(User).filter(User.username == username))
        return res.scalars().first()

    async def get_by_username_or_email(
        self, db: AsyncSession, username: str, email: str
    ) -> User | None:
        res = await db.execute(
            select(User).filter((User.username == username) | (User.email == email))
        )
        return res.scalars().first()


user_repo = UserRepository(User)
