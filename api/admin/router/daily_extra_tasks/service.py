import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.daily_extra_task import AdminDailyExtraTaskCRUD


class AdminDailyExtraTaskService(
    AdminGenericService[
        schemas.DailyExtraTaskCreate,
        schemas.DailyExtraTaskUpdate,
        schemas.DailyExtraTaskResponse,
        schemas.AdminGetListParams,
        AdminDailyExtraTaskCRUD]
):

    response_schema = schemas.DailyExtraTaskResponse
    entity_name = "daily_extra_task"
    crud_cls = AdminDailyExtraTaskCRUD
