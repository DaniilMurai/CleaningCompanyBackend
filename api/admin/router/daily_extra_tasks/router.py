from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.params import Depends

import schemas
from api.admin.router.daily_extra_tasks.service import AdminDailyExtraTaskService

router = APIRouter(prefix="/daily-extra-tasks", tags=["daily extra tasks"])


@router.get("/")
async def get_daily_extra_tasks(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminDailyExtraTaskService = Depends()
) -> list[schemas.DailyExtraTaskResponse]:
    return await service.get_list(params)


@router.post("/")
async def create_daily_extra_task(
        data: schemas.DailyExtraTaskCreate,
        service: AdminDailyExtraTaskService = Depends()
) -> schemas.DailyExtraTaskResponse:
    return await service.create(data)


@router.patch("/")
async def edit_daily_extra_task(
        daily_extra_task_id: int,
        data: schemas.DailyExtraTaskUpdate,
        service: AdminDailyExtraTaskService = Depends()
) -> schemas.DailyExtraTaskResponse:
    return await service.update(daily_extra_task_id, data)


@router.delete("/")
async def delete_daily_extra_task(
        daily_extra_task_id: int,
        service: AdminDailyExtraTaskService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(daily_extra_task_id)
