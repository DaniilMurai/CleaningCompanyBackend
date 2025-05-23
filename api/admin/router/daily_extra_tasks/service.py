import exceptions
import schemas
from db.crud.admin.daily_extra_task import AdminDailyExtraTaskCRUD


class AdminDailyExtraTaskService:
    def __init__(
            self,
            crud: AdminDailyExtraTaskCRUD.depends()
    ):
        self.crud: AdminDailyExtraTaskCRUD = crud

    async def get_daily_extra_tasks(self, params: schemas.DailyExtraTaskUpdate) -> \
            list[schemas.DailyExtraTaskResponse]:
        kwargs = params.model_dump(exclude_none=True) if params else {}
        daily_extra_tasks = await self.crud.get_list(**kwargs)
        return [schemas.DailyExtraTaskResponse.model_validate(daily_extra_tasks) for
                daily_extra_tasks in daily_extra_tasks]

    async def create_daily_extra_task(
            self, data: schemas.DailyExtraTaskCreate
    ) -> schemas.DailyExtraTaskResponse:
        daily_extra_tasks = await self.crud.create(**data.model_dump(exclude_none=True))
        return schemas.DailyExtraTaskResponse.model_validate(daily_extra_tasks)

    async def update_daily_extra_task(
            self, daily_extra_tasks_id: int, data: schemas.DailyExtraTaskUpdate
    ) -> schemas.DailyExtraTaskResponse:
        daily_extra_tasks = await self.crud.get(daily_extra_tasks_id)
        if not daily_extra_tasks:
            raise exceptions.ObjectNotFoundByIdError(
                "daily_extra_tasks", daily_extra_tasks_id
            )

        data_to_update = data.model_dump(exclude_none=True)

        daily_extra_tasks = await self.crud.update(daily_extra_tasks, data_to_update)
        return schemas.DailyExtraTaskResponse.model_validate(daily_extra_tasks)

    async def delete_daily_extra_task(
            self, daily_extra_tasks_id: int
    ) -> schemas.SuccessResponse:
        daily_extra_tasks = await self.crud.get(daily_extra_tasks_id)
        if not daily_extra_tasks:
            raise exceptions.ObjectNotFoundByIdError(
                "daily_extra_tasks", daily_extra_tasks_id
            )

        await self.crud.delete(daily_extra_tasks_id)
        return schemas.SuccessResponse(success=True)
