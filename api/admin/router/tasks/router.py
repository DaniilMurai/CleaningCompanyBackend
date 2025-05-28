from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.tasks.service import AdminTaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def get_tasks(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminTaskService = Depends()
) -> list[schemas.TaskResponse]:
    return await service.get_list(params)


@router.post("/")
async def create_task(
        data: schemas.TaskCreate,
        service: AdminTaskService = Depends()
) -> schemas.TaskResponse:
    return await service.create(data)


@router.patch("/")
async def edit_task(
        task_id: int,
        data: schemas.TaskUpdate,
        service: AdminTaskService = Depends()
) -> schemas.TaskResponse:
    return await service.update(task_id, data)


@router.delete("/")
async def delete_task(
        task_id: int,
        service: AdminTaskService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(task_id)
