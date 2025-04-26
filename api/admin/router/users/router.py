from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.users.service import AdminUsersService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users(
        params: Annotated[schemas.GetUsersParams, Query()],
        admin_service: AdminUsersService = Depends(),
) -> list[schemas.UserSchema]:
    return await admin_service.get_users(params)


@router.post("/")
async def create_user(
        userdata: schemas.RegisterUserData,
        admin_service: AdminUsersService = Depends(),
):
    return await admin_service.create_user(userdata)


@router.patch("/")
async def update_user(
        user_id: int,
        userdata: schemas.UserUpdateData,
        admin_service: AdminUsersService = Depends()
):
    return await admin_service.update_user(user_id, userdata)


@router.delete("/")
async def delete_user(
        user_id: int,
        admin_service: AdminUsersService = Depends()
):
    return await admin_service.delete_user(user_id)
