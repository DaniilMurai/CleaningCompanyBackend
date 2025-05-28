import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.room import AdminRoomCRUD


class AdminRoomService(
    AdminGenericService[
        schemas.RoomCreate,
        schemas.RoomUpdate,
        schemas.RoomResponse,
        schemas.AdminGetListParams,
        AdminRoomCRUD,
    ]
):

    response_schema = schemas.RoomResponse
    entity_name = "room"
    crud_cls = AdminRoomCRUD
