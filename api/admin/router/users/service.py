import exceptions
import schemas
from api.admin.base.service import AdminUserDepend
from config import settings
from db.crud import AdminUsersCRUD
from schemas import UserRole
from utils.security.tokens import create_invite_token


class AdminUsersService:
    def __init__(
            self,
            admin: AdminUserDepend,
            crud: AdminUsersCRUD.depends()
    ):
        self.admin = admin
        self.crud: AdminUsersCRUD = crud

    def check_access_to_role(self, role: schemas.UserRole):
        if role == schemas.UserRole.superadmin:
            raise exceptions.CreateUserWithRoleForbiddenError(role)
        if self.admin.role == schemas.UserRole.admin and role == UserRole.admin:
            raise exceptions.CreateUserWithRoleForbiddenError(role)

    async def get_users(self, params: schemas.GetUsersParams | None = None):
        kwargs = params.model_dump(exclude_none=True) if params else {}
        return await self.crud.get_list(**kwargs)

    async def create_user(self, data: schemas.RegisterUserData) -> schemas.InviteLink:
        self.check_access_to_role(data.role)

        user = await self.crud.create(
            **data.model_dump(exclude_unset=True),
            status=schemas.UserStatus.pending,
        )
        await self.crud.db.commit()

        token = create_invite_token({"sub": user.id, "type": "invite"})
        return schemas.InviteLink(
            invite_link=(f"{settings.FRONTEND_URL}/activate?token="
                         f"{token}")
        )

    async def update_user(
            self,
            user_id: int,
            userdata: schemas.UserUpdateData
    ) -> schemas.UserSchema:
        user = await self.crud.get(user_id)
        if not user:
            raise exceptions.ObjectNotFoundByIdError("user", user_id)

        data_to_update = userdata.model_dump(
            exclude_none=True
        )
        user = await self.crud.update(
            user, data_to_update
        )

        await self.crud.db.commit()
        return schemas.UserSchema.model_validate(user)

    async def delete_user(self, user_id: int):
        await self.crud.delete(user_id)
        await self.crud.db.commit()
        return schemas.SuccessResponse(success=True)
