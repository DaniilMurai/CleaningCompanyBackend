import schemas
from db.crud.admin.task import AdminTaskCRUD
from exceptions import ObjectNotFoundByIdError


class AdminTaskService:

    def __init__(
            self,
            crud: AdminTaskCRUD.depends()
    ):
        self.crud: AdminTaskCRUD = crud

    async def get_tasks(self, params: schemas.TaskUpdate | None = None) -> list[
        schemas.TaskResponse]:
        tasks = await self.crud.get_list(**params.model_dump(exclude_none=True))
        return [schemas.TaskResponse.model_validate(task) for task in tasks]

    async def create_task(self, data: schemas.TaskCreate) -> schemas.TaskResponse:
        task = await self.crud.create(**data.model_dump(exclude_none=True))
        return schemas.TaskResponse.model_validate(task)

    async def update_task(
            self, task_id: int, data: schemas.TaskUpdate
    ) -> schemas.TaskResponse:
        task = await self.crud.get(task_id)
        if not task:
            raise ObjectNotFoundByIdError("tasks", task_id)

        task = await self.crud.update(task, **data.model_dump(exclude_none=True))
        return schemas.TaskResponse.model_validate(task)

    async def delete_task(self, task_id: int) -> schemas.SuccessResponse:
        task = await self.crud.get(task_id)
        if not task:
            raise ObjectNotFoundByIdError("tasks", task_id)

        await self.crud.delete(task_id)

        return schemas.SuccessResponse(success=True)
