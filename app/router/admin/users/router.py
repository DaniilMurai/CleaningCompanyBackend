from fastapi import APIRouter

from app.dependecies.dependecies import AdminServiceDependency
from app.schemas.UserSchema import RegisterUser, UserUpdate
from app.services.admin_service import AdminService

router = APIRouter(prefix="/users")


@router.get("")
async def get_user(admin_service: AdminService = AdminServiceDependency):
    return await admin_service.get_users()


@router.post("")
async def create_user(
        userdata: RegisterUser,
        admin_service: AdminService = AdminServiceDependency,
):
    return await admin_service.create_user(userdata)


@router.patch("")
async def edit_user(
        user_id: int,
        userdata: UserUpdate,
        admin_service: AdminService = AdminServiceDependency
):
    return await admin_service.edit_user(user_id, userdata)


@router.delete("")
async def delete_user(
        user_id: int,
        admin_service: AdminService = AdminServiceDependency
):
    return await admin_service.delete_user(user_id)
