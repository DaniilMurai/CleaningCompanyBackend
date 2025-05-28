import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.location import AdminLocationsCRUD


class AdminLocationService(
    AdminGenericService[
        schemas.LocationCreate,
        schemas.LocationUpdate,
        schemas.LocationResponse,
        schemas.AdminGetListParams,
        AdminLocationsCRUD]
):

    response_schema = schemas.LocationResponse
    entity_name = "location"
    crud_cls = AdminLocationsCRUD
