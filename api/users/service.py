from typing import Annotated

from fastapi import Depends

import exceptions
import schemas.base
from db.crud import UserCRUD
from schemas import UserUpdatePassword, UserdataUpdate
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

        await self.crud.update(
            self.user, password=data.new_password
        )  # TODO не работает

        return schemas.SuccessResponse(success=True)

    async def change_userdata(self, data: UserdataUpdate):

        await self.crud.validate_nickname(data.nickname, self.user.id)

        # TODO не работает
        await self.crud.update(
            self.user, nickname=data.nickname, full_name=data.full_name
        )  # TODO если одно из полей не передано оно будет none, такого не должно
        # TODO быть, в функцию update нужно добавить exclude_none или чет такое

        return schemas.SuccessResponse(success=True)
