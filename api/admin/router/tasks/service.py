import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.task import AdminTaskCRUD


class AdminTaskService(
    AdminGenericService[
        schemas.TaskCreate,
        schemas.TaskUpdate,
        schemas.TaskResponse,
        schemas.AdminGetListParams,
        AdminTaskCRUD]
):

    response_schema = schemas.TaskResponse
    entity_name = "task"
    crud_cls = AdminTaskCRUD
