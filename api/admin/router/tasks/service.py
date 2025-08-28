import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.task import AdminTaskCRUD
from schemas import AdminGetListParams


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

    async def get_task_with_hints(self, params: AdminGetListParams | None = None) -> \
            list[schemas.TaskWithHintsResponse]:
        tasks = await self.crud.get_tasks_with_hints(params)

        return [schemas.TaskWithHintsResponse.model_validate(t) for t in
                tasks]
