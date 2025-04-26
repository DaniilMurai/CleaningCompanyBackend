from typing import Annotated

from fastapi import Depends

import exceptions
import schemas.base
from db.crud import UserCRUD
from schemas import UserUpdatePassword
from utils.password import verify_password
from .base.service import UserDepend


class UsersService:
    def __init__(
            self,
            user: UserDepend,
            crud: Annotated[UserCRUD, Depends()]
    ):
        self.user = user
        self.crud = crud

    def get_current_user(self):
        return self.user

    async def change_password(self, data: UserUpdatePassword):

        if not verify_password(data.old_password, self.user.hashed_password):
            raise exceptions.WrongPassword(data.old_password)

        async with self.crud.db.begin():
            await self.crud.update(self.user, password=data.new_password)
        await self.crud.db.refresh(self.user)

        return schemas.SuccessResponse(success=True)
