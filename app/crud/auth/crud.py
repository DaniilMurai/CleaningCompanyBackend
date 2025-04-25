from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.User.model import User


class AuthCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalars().one_or_none()
