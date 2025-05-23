import exceptions
import schemas
from db.crud.admin.room_task import AdminRoomTaskCRUD


class AdminRoomTaskService:
    def __init__(
            self,
            crud: AdminRoomTaskCRUD.depends()
    ):
        self.crud: AdminRoomTaskCRUD = crud

    async def get_room_tasks(self, params: schemas.RoomTaskUpdate) -> list[
        schemas.RoomTaskResponse]:
        kwargs = params.model_dump(exclude_none=True) if params else {}
        room_tasks = await self.crud.get_list(**kwargs)
        return [schemas.RoomTaskResponse.model_validate(room_task) for room_task in
                room_tasks]

    async def create_room_task(  # TODO Сделать проверку если нет room_id или task_id
            self, data: schemas.RoomTaskCreate
    ) -> schemas.RoomTaskResponse:
        room_task = await self.crud.create(**data.model_dump(exclude_none=True))
        return schemas.RoomTaskResponse.model_validate(room_task)

    async def update_room_task(
            self, room_task_id: int, data: schemas.RoomTaskUpdate
    ) -> schemas.RoomTaskResponse:
        room_task = await self.crud.get(room_task_id)
        if not room_task:
            raise exceptions.ObjectNotFoundByIdError("room_tasks", room_task_id)

        date_to_update = data.model_dump(exclude_none=True)

        room_task = await self.crud.update(room_task, date_to_update)
        return schemas.RoomTaskResponse.model_validate(room_task)

    async def delete_room_task(self, room_task_id: int) -> schemas.SuccessResponse:
        room_task = await self.crud.get(room_task_id)
        if not room_task:
            raise exceptions.ObjectNotFoundByIdError("room_tasks", room_task_id)

        await self.crud.delete(room_task_id)
        return schemas.SuccessResponse(success=True)
