from sqlalchemy import select

from .base import CRUD
from ..models import User


class AuthCRUD(CRUD):
    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalars().one_or_none()
