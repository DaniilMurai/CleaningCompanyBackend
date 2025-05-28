from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.room_tasks.service import AdminRoomTaskService

router = APIRouter(prefix="/room-tasks", tags=["room tasks"])


@router.get("/")
async def get_room_tasks(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminRoomTaskService = Depends()
) -> list[schemas.RoomTaskResponse]:
    return await service.get_list(params)


@router.post("/")
async def create_room_task(
        data: schemas.RoomTaskCreate,
        service: AdminRoomTaskService = Depends()
) -> schemas.RoomTaskResponse:
    return await service.create(data)


@router.patch("/")
async def edit_room_task(
        room_task_id: int,
        data: schemas.RoomTaskUpdate,
        service: AdminRoomTaskService = Depends()
) -> schemas.RoomTaskResponse:
    return await service.update(room_task_id, data)


@router.delete("/")
async def delete_room_task(
        room_task_id: int,
        service: AdminRoomTaskService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(room_task_id)
