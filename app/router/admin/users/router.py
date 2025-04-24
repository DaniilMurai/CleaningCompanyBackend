from typing import Literal

from fastapi import APIRouter, Query

from app.dependecies.dependecies import AdminServiceDependency
from app.services.admin_service import AdminService

router = APIRouter(prefix="/users")


@router.get("")
async def get_user(
        search_by: Literal[
            "id", "nick_name", "role", "full_name", "description_from_admin", "created_at"
        ] = Query(None),
        admin_service: AdminService = AdminServiceDependency):
    return await admin_service.get_users(search_by)


@router.post("")
async def create_user():
    return "user created"


@router.patch("")
async def edit_user():
    return "user edited"


@router.delete("")
async def delete_user():
    return "user deleted"
