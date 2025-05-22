from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.room_tasks.service import AdminRoomTaskService

router = APIRouter(prefix="/room-tasks", tags=["Room Tasks"])


@router.get("/")
async def get_room_tasks(
        params: Annotated[schemas.RoomTaskCreate, Query()],  # TODO Схема ?
        service: AdminRoomTaskService = Depends()
) -> list[schemas.RoomTaskResponse]:
    pass


@router.post("/")
async def create_room_task(
        data: schemas.RoomTaskCreate,
        service: AdminRoomTaskService = Depends()
) -> schemas.RoomTaskResponse:
    pass


@router.patch("/")
async def edit_room_task(
        room_task_id: int,
        data: schemas.RoomTaskCreate,  # TODO Схема ?
        service: AdminRoomTaskService = Depends()
) -> schemas.RoomTaskResponse:
    pass


@router.delete("/")
async def delete_room_task(
        room_task_id: int,
        service: AdminRoomTaskService = Depends()
) -> schemas.SuccessResponse:
    pass
