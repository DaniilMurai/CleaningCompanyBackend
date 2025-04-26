from sqlalchemy import exists, select

import exceptions
from utils.password import validate_password_and_generate_hash
from .base import BaseModelCrud
from ...models import User


class UserCRUD(BaseModelCrud[User]):
    model = User
    search_fields = ("nickname", "full_name", "admin_note")

    async def pre_process_data(self, data: dict) -> dict:
        if "nickname" in data:
            data["nickname"] = await self.validate_nickname(data["nickname"])
        if "password" in data:
            data["hashed_password"] = validate_password_and_generate_hash(
                data.pop("password")
            )
        return data

    def pre_process_update_data(self, data: dict):
        return self.pre_process_data(data)

    def pre_process_create_data(self, data: dict):
        return self.pre_process_data(data)

    async def validate_nickname(
            self, nickname: str | None,
            exclude_user_id: int | None = None,
    ):
        if not nickname:
            raise exceptions.NicknameCannotBeEmptyError()

        nickname = nickname.strip()

        stmt = exists().where(self.model.nickname == nickname)
        if exclude_user_id:
            stmt = stmt.where(self.model.id != exclude_user_id)

        if await self.db.scalar(select(stmt)):
            raise exceptions.NicknameAlreadyExists(nickname)
        return nickname
