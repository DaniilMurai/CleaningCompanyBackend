from sqlalchemy import select

from db.models import User
from ..models import UserCRUD


class AdminUsersCRUD(UserCRUD):
    async def get_users(self):
        users = await self.db.execute(select(User))
        return users.scalars().all()
