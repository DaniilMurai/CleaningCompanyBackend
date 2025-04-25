from fastapi import HTTPException

from app.core.config import settings
from app.crud.admin.crud import AdminCRUD
from app.schemas.UserSchema import RegisterUser, UserUpdate
from app.security.tokens import create_invite_token


class AdminService:
    def __init__(self, admin_crud: AdminCRUD):
        self.admin_crud = admin_crud

    async def get_users(self):
        return await self.admin_crud.get_users()

    async def create_user(self, userdata: RegisterUser):
        user = await self.admin_crud.create_user(userdata)
        token = create_invite_token({"sub": user.id, "type": "invite"})
        return {"invite_link": f"{settings.FRONTEND_URL}/activate?token={token}"}

    async def edit_user(
            self,
            user_id: int,
            userdata: UserUpdate
    ):
        if not any(
                [userdata.nickname, userdata.hashed_password, userdata.role,
                 userdata.full_name, userdata.admin_note]
        ):
            raise HTTPException(status_code=400, detail="No fields to update provided")

        async with self.admin_crud.db.begin():
            db_user = await self.admin_crud.get_user_by_id(user_id)

            fields_to_update = {}

            if userdata.nickname is not None:
                fields_to_update["nickname"] = userdata.nickname
            if userdata.role is not None:
                fields_to_update["role"] = userdata.role
            if userdata.full_name is not None:
                fields_to_update["full_name"] = userdata.full_name
            if userdata.admin_note is not None:
                fields_to_update[
                    "admin_note"] = userdata.admin_note

            if fields_to_update:
                db_user = await self.admin_crud.update_user_fields(
                    db_user, **fields_to_update
                )

            if userdata.hashed_password is not None:
                db_user = await self.admin_crud.update_user_password(
                    db_user, userdata.hashed_password
                )

        # здесь транзакция уже закоммичена
        await self.admin_crud.db.refresh(db_user)

        return db_user

    async def delete_user(self, user_id: int):
        return await self.admin_crud.delete_user(user_id)
