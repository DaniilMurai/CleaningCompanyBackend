import exceptions
import schemas
from db.crud.admin.room import AdminRoomCRUD


class AdminRoomService:

    def __init__(
            self,
            crud: AdminRoomCRUD.depends()
    ):
        self.crud: AdminRoomCRUD = crud

    async def get_rooms(self, params: schemas.RoomUpdate | None = None) -> list[
        schemas.RoomResponse]:
        kwargs = params.model_dump(exclude_none=True) if params else {}
        rooms = await self.crud.get_list(**kwargs)
        return [schemas.RoomResponse.model_validate(r) for r in rooms]

    async def create_room(self, data: schemas.RoomCreate) -> schemas.RoomResponse:
        room = await self.crud.create(**data.model_dump(exclude_none=True))
        return schemas.RoomResponse.model_validate(room)

    async def update_room(
            self, room_id: int, data: schemas.RoomUpdate
    ) -> schemas.RoomResponse:
        room = await self.crud.get(room_id)

        if not room:
            raise exceptions.ObjectNotFoundByIdError("room", room_id)

        data_to_update = data.model_dump(exclude_none=True)

        room = await self.crud.update(room, data_to_update)

        return schemas.RoomResponse.model_validate(room)

    async def delete_room(self, room_id: int) -> schemas.SuccessResponse:
        room = await self.crud.get(room_id)
        if not room:
            raise exceptions.ObjectNotFoundByIdError("room", room_id)

        await self.crud.delete(room_id)
        return schemas.SuccessResponse(success=True)
