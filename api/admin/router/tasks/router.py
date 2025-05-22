from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.tasks.service import AdminTaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
async def get_tasks(
        params: Annotated[schemas.TaskUpdate, Query()],
        service: AdminTaskService = Depends()
) -> list[schemas.TaskResponse]:
    return await service.get_tasks(params)


@router.post("/")
async def create_task(
        data: schemas.TaskCreate,
        service: AdminTaskService = Depends()
) -> schemas.TaskResponse:
    return await service.create_task(data)


@router.patch("/")
async def edit_task(
        task_id: int,
        data: schemas.TaskUpdate,
        service: AdminTaskService = Depends()
) -> schemas.TaskResponse:
    return await service.update_task(task_id, data)


@router.delete("/")
async def delete_task(
        task_id: int,
        service: AdminTaskService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete_task(task_id)
