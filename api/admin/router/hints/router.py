from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.hints.service import AdminHintService

router = APIRouter(prefix="/hints", tags=["hints"])


@router.get("/")
async def get_hints(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminHintService = Depends()
) -> list[schemas.HintsResponse]:
    return await service.get_list(params)


@router.get("/{task_id}")
async def get_hint_by_task_id(
        task_id: int,
        service: AdminHintService = Depends()
) -> list[schemas.HintsResponse]:
    return await service.get_hints_by_task_id(task_id)


@router.post("/")
async def create_hint(
        data: schemas.HintsCreate,
        service: AdminHintService = Depends()
) -> schemas.HintsResponse:
    return await service.create_hint(data)


@router.patch("/")
async def update_hint(
        hint_id: int,
        data: schemas.HintsUpdate,
        service: AdminHintService = Depends()
) -> schemas.HintsResponse:
    return await service.update_hint(hint_id, data)


@router.delete("/")
async def delete_hint(
        hint_id: int,
        service: AdminHintService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(hint_id)
