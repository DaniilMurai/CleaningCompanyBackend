from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.inventories.service import AdminInventoryService

router = APIRouter(prefix="/inventories", tags=["inventories"])


@router.get("/")
async def get_inventories(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminInventoryService = Depends()
) -> list[schemas.InventoryResponse]:
    return await service.get_list(params)


@router.get("/{task_id}")
async def get_inventory_by_task_id(
        task_id: int,
        service: AdminInventoryService = Depends()
) -> list[schemas.InventoryResponse]:
    return await service.get_inventories_by_task_id(task_id)


@router.post("/")
async def create_inventory(
        data: schemas.InventoryCreate,
        service: AdminInventoryService = Depends()
) -> schemas.InventoryResponse:
    return await service.create_inventory(data)


@router.patch("/")
async def update_inventory(
        inventory_id: int,
        data: schemas.InventoryUpdate,
        service: AdminInventoryService = Depends()
) -> schemas.InventoryResponse:
    return await service.update_inventory(inventory_id, data)


@router.delete("/")
async def delete_inventory(
        inventory_id: int,
        service: AdminInventoryService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(inventory_id)
