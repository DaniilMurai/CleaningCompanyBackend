from fastapi import APIRouter
from fastapi.params import Depends

import schemas
from api.users.service import UsersService
from schemas import UserUpdatePassword

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_current_user(service: UsersService = Depends()) -> schemas.UserSchema:
    return service.get_current_user()


@router.post("/change_password")
async def change_password(
        data: UserUpdatePassword,
        service: UsersService = Depends()
) -> schemas.SuccessResponse:
    return await service.change_password(data)
