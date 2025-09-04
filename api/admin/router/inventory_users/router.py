from typing import Annotated

from fastapi import APIRouter, Depends, Query

import schemas
from api.admin.router.inventory_users.service import AdminInventoryUserService

router = APIRouter(prefix="/inventory_users", tags=["inventory_users"])


@router.get("/")
async def get_inventory_users(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminInventoryUserService = Depends()
) -> list[schemas.InventoryUserResponse]:
    return await service.get_list(params)


@router.post("/")
async def create_inventory_user(
        data: schemas.InventoryUserCreate,
        service: AdminInventoryUserService = Depends()
) -> schemas.InventoryUserResponse:
    return await service.create(data)


@router.patch("/")
async def edit_inventory_user(
        inventory_user_id: int,
        data: schemas.InventoryUserUpdate,
        service: AdminInventoryUserService = Depends()
) -> schemas.InventoryUserResponse:
    return await service.update(inventory_user_id, data)


@router.delete("/")
async def delete_inventory_user(
        inventory_user_id: int,
        service: AdminInventoryUserService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(inventory_user_id)
