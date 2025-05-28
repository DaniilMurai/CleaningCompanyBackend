import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.room_task import AdminRoomTaskCRUD


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

# TODO Сделать проверку если нет room_id или task_id для create, update
