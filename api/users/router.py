from fastapi import APIRouter
from fastapi.params import Depends

import schemas
from api.users.service import UsersService
from schemas import UpdateUserData, UserUpdatePassword

router = APIRouter(tags=["users"])


@router.get("/me")
async def get_current_user(service: UsersService = Depends()) -> schemas.UserSchema:
    return service.get_current_user()


@router.post("/me")
async def update_current_user(
        data: UpdateUserData,
        service: UsersService = Depends()
) -> schemas.UserSchema:
    return await service.update_current_user(data)


@router.post("/change_password")
async def change_password(
        data: UserUpdatePassword,
        service: UsersService = Depends()
) -> schemas.SuccessResponse:
    return await service.change_password(data)


@router.get("/daily-assignment")
async def get_daily_assignment(
        service: UsersService = Depends()
) -> list[schemas.DailyAssignmentForUserResponse]:
    return await service.get_daily_assignment()
