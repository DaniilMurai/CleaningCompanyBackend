import exceptions
import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.room import AdminRoomCRUD
from db.crud.admin.room_task import AdminRoomTaskCRUD
from db.crud.admin.task import AdminTaskCRUD


class AdminRoomTaskService(
    AdminGenericService[
        schemas.RoomTaskCreate,
        schemas.RoomTaskUpdate,
        schemas.RoomTaskResponse,
        schemas.AdminGetListParams,
        AdminRoomTaskCRUD]
):

    response_schema = schemas.RoomTaskResponse
    entity_name = "room_task"
    crud_cls = AdminRoomTaskCRUD

    async def create_room_task(
            self, data: schemas.RoomTaskCreate
    ) -> schemas.RoomTaskResponse:
        await self.validate(data)
        return await self.create(data)

    async def update_room_task(
            self,
            room_task_id: int,
            data: schemas.RoomTaskUpdate
    ) -> schemas.RoomTaskResponse:
        await self.validate(data)
        return await self.update(room_task_id, data)

    async def validate(self, data: schemas.BaseRoomTask):
        room_crud = AdminRoomCRUD(self.crud.db)  # Не работает
        task_crud = AdminTaskCRUD(self.crud.db)  # Не работает

        room = await room_crud.get(data.room_id)
        task = await task_crud.get(data.task_id)

        if not room:
            raise exceptions.ObjectNotFoundByIdError("room", data.room_id)
        if not task:
            raise exceptions.ObjectNotFoundByIdError("task", data.task_id)

        return data

# TODO Поменять Validate
