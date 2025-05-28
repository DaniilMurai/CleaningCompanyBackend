import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.daily_assignment import AdminDailyAssignmentCRUD


class AdminDailyAssignmentService(
    AdminGenericService[
        schemas.DailyAssignmentCreate,
        schemas.DailyAssignmentUpdate,
        schemas.DailyAssignmentResponse,
        schemas.AdminGetListParams,
        AdminDailyAssignmentCRUD]
):

    response_schema = schemas.DailyAssignmentResponse
    entity_name = "daily_assignment"
    crud_cls = AdminDailyAssignmentCRUD
