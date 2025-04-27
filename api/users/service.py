import exceptions
import schemas.base
from db.crud import UserCRUD
from schemas import UpdateUserData, UserUpdatePassword
from utils.password import verify_password
from .base.service import UserDepend


class UsersService:
    def __init__(
            self,
            user: UserDepend,
            crud: UserCRUD.depends()
    ):
        self.user = user
        self.crud = crud

    def get_current_user(self):
        return self.user

    async def change_password(self, data: UserUpdatePassword):
        if not verify_password(data.old_password, self.user.hashed_password):
            raise exceptions.WrongPasswordError(data.old_password)

        await self.crud.update(
            self.user, password=data.new_password
        )
        await self.crud.db.commit()

        return schemas.SuccessResponse(success=True)

    async def update_current_user(self, data: UpdateUserData):
        await self.crud.update(
            self.user, **data.model_dump(exclude_none=True)
        )
        await self.crud.db.commit()

        return self.user
