from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.rooms.service import AdminRoomService

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/")
async def get_rooms(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminRoomService = Depends(),
) -> list[schemas.RoomResponse]:
    return await service.get_list(params)


@router.post("/")
async def create_room(
        data: schemas.RoomCreate,
        service: AdminRoomService = Depends(),
) -> schemas.RoomResponse:
    return await service.create(data)


@router.patch("/")
async def edit_room(
        room_id: int,
        data: schemas.RoomUpdate,
        service: AdminRoomService = Depends(),
) -> schemas.RoomResponse:
    return await service.update(room_id, data)


@router.delete("/")
async def delete_room(
        room_id: int,
        service: AdminRoomService = Depends(),
) -> schemas.SuccessResponse:
    return await service.delete(room_id)
