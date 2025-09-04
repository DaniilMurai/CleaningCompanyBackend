import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.inventory_user import AdminInventoryUserCRUD


class AdminInventoryUserService(
    AdminGenericService[
        schemas.InventoryUserCreate,
        schemas.InventoryUserUpdate,
        schemas.InventoryUserResponse,
        schemas.AdminGetListParams,
        AdminInventoryUserCRUD
    ]
):
    response_schema = schemas.InventoryUserResponse
    entity_name = "inventory_user"
    crud_cls = AdminInventoryUserCRUD
