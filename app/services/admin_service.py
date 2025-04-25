from fastapi import HTTPException

from app.crud.admin.crud import AdminCRUD
from app.schemas.UserSchema import UserCreate, UserUpdate


class AdminService:
    def __init__(self, admin_crud: AdminCRUD):
        self.admin_crud = admin_crud

    async def get_users(self):
        return await self.admin_crud.get_users()

    async def create_user(self, userdata: UserCreate):
        return await self.admin_crud.create_user(userdata)

    async def edit_user(
            self,
            user_id: int,
            userdata: UserUpdate
    ):
        if not any([userdata.nick_name, userdata.password, userdata.role,
                    userdata.full_name, userdata.description_from_admin]):
            raise HTTPException(status_code=400, detail="No fields to update provided")

        async with self.admin_crud.db.begin():
            db_user = await self.admin_crud.get_user_by_id(user_id)

            fields_to_update = {}

            if userdata.nick_name is not None:
                fields_to_update["nick_name"] = userdata.nick_name
            if userdata.role is not None:
                fields_to_update["role"] = userdata.role
            if userdata.full_name is not None:
                fields_to_update["full_name"] = userdata.full_name
            if userdata.description_from_admin is not None:
                fields_to_update["description_from_admin"] = userdata.description_from_admin

            if fields_to_update:
                db_user = await self.admin_crud.update_user_fields(db_user, **fields_to_update)

            if userdata.password is not None:
                db_user = await self.admin_crud.update_user_password(db_user, userdata.password)

        # здесь транзакция уже закоммичена
        await self.admin_crud.db.refresh(db_user)

        return db_user

    async def delete_user(self, user_id: int):
        return await self.admin_crud.delete_user(user_id)
