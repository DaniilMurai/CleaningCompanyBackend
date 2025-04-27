from sqlalchemy import exists, select

import exceptions
from utils.db import statement_to_str
from utils.password import validate_password_and_generate_hash
from .base import BaseModelCrud
from ...models import User


class UserCRUD(BaseModelCrud[User]):
    model = User
    search_fields = ("nickname", "full_name", "admin_note")

    async def pre_process_data(
            self, data: dict,
            current_obj_id: int | None = None
    ) -> dict:
        if "nickname" in data:
            data["nickname"] = await self.validate_nickname(
                data["nickname"], current_obj_id
            )
        if "password" in data:
            data["hashed_password"] = validate_password_and_generate_hash(
                data.pop("password")
            )
        return data

    def pre_process_update_data(
            self, data: dict,
            current_obj_id: int | None = None
    ):
        return self.pre_process_data(data, current_obj_id)

    def pre_process_create_data(self, data: dict):
        return self.pre_process_data(data)

    async def validate_nickname(
            self, nickname: str | None,
            exclude_user_id: int | None = None,
    ) -> str:
        if not nickname:
            raise exceptions.NicknameCannotBeEmptyError()

        nickname = nickname.strip()

        conditions = [
            self.model.nickname == nickname
        ]
        if exclude_user_id:
            conditions.append(self.model.id != exclude_user_id)

        stmt = select(exists().where(*conditions))

        print(statement_to_str(stmt))

        if await self.db.scalar(stmt):
            raise exceptions.NicknameAlreadyExists(nickname)
        return nickname
