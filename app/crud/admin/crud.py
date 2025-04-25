from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.User.model import User, UserStatus
from app.schemas.UserSchema import RegisterUser
from app.utils.password.functions import get_password_hash, verify_password


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
            raise HTTPException(
                status_code=409, detail=f"User with {fields_str} already exists"
            )

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
            raise HTTPException(
                status_code=409,
                detail=f"New values for {fields_str} match the current ones"
            )

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

        if verify_password(new_password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You can't change the password to the one you have"
            )

        db_user.hashed_password = get_password_hash(new_password)
        return db_user

    async def get_users(self):
        users = await self.db.execute(select(User))
        return users.scalars().all()

    async def create_user(self, userdata: RegisterUser):
        try:
            if not userdata:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="No userdata"
                )

            new_user = User(
                nickname=userdata.nickname,
                hashed_password=get_password_hash(userdata.password),
                role=userdata.role,
                status=UserStatus.pending,
                full_name=userdata.full_name,
                admin_note=userdata.admin_note,

            )

            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)

            return new_user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}"
            )

    async def delete_user(self, user_id: int):
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Удаляем пользователя
            await self.db.delete(user)
            await self.db.commit()

            return {"success": True}

        except Exception as e:
            await self.db.rollback()  # важно при ошибках
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {e}"
            )
