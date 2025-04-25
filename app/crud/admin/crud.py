from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.User.model import User
from app.schemas.UserSchema import UserCreate
from app.utils.password.functions import get_password_hash


class AdminCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_unique_fields(self, exclude_user_id: int = None, **kwargs):
        query = select(User)

        for field, value in kwargs.items():
            query = query.where(getattr(User, field) == value)

        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)

        result = await self.db.execute(query)
        if result.scalars().first():
            fields_str = ', '.join(f"{key}='{value}'" for key, value in kwargs.items())
            raise HTTPException(status_code=409, detail=f"User with {fields_str} already exists")

    async def get_user_by_id(self, user_id: int):
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalars().first()

    async def update_user_fields(self, user: User, **fields_to_update):
        same_fields = [
            field for field, value in fields_to_update.items()
            if getattr(user, field) == value
        ]
        if same_fields:
            fields_str = ', '.join(same_fields)
            raise HTTPException(status_code=409, detail=f"New values for {fields_str} match the current ones")

        await self._check_unique_fields(exclude_user_id=user.id, **fields_to_update)

        for field, value in fields_to_update.items():
            setattr(user, field, value)

        return user

    async def update_user_password(self, db_user: User, new_password: str):
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if new_password != db_user.password:
            db_user.password = get_password_hash(new_password)
            return db_user

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can't change the password to the one you have"
        )

    async def get_users(self):
        users = await self.db.execute(select(User))
        return users.scalars().all()

    async def create_user(self, userdata: UserCreate):
        try:
            if not userdata:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No userdata")

            new_user = User(
                nick_name=userdata.nick_name,
                password=get_password_hash(userdata.password),
                role=userdata.role,
                full_name=userdata.full_name,
                description_from_admin=userdata.description_from_admin,

            )

            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(userdata)

            return new_user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}"
            )

    async def delete_user(self, user_id: int):
        try:
            user = await self.db.execute(select(User).where(User.id == user_id))
            user = user.scalars().first()

            await self.db.delete(user)

            await self.db.commit()
            await self.db.refresh(user)

            return {"success": True}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}"
            )
