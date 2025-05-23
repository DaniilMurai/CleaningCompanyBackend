import exceptions
import schemas
from db.crud.admin.daily_assignment import AdminDailyAssignmentCRUD


class AdminDailyAssignmentService:
    def __init__(
            self,
            crud: AdminDailyAssignmentCRUD.depends()
    ):
        self.crud: AdminDailyAssignmentCRUD = crud

    async def get_daily_assignments(self, params: schemas.DailyAssignmentUpdate) -> \
            list[schemas.DailyAssignmentResponse]:
        kwargs = params.model_dump(exclude_none=True) if params else {}
        daily_assignments = await self.crud.get_list(**kwargs)
        return [schemas.DailyAssignmentResponse.model_validate(daily_assignment) for
                daily_assignment in daily_assignments]

    async def create_daily_assignment(
            self, data: schemas.DailyAssignmentCreate
    ) -> schemas.DailyAssignmentResponse:
        daily_assignment = await self.crud.create(**data.model_dump(exclude_none=True))
        return schemas.DailyAssignmentResponse.model_validate(daily_assignment)

    async def update_daily_assignment(
            self, daily_assignment_id: int, data: schemas.DailyAssignmentUpdate
    ) -> schemas.DailyAssignmentResponse:
        daily_assignment = await self.crud.get(daily_assignment_id)
        if not daily_assignment:
            raise exceptions.ObjectNotFoundByIdError(
                "daily_assignment", daily_assignment_id
            )

        data_to_update = data.model_dump(exclude_none=True)

        daily_assignment = await self.crud.update(daily_assignment, data_to_update)
        return schemas.DailyAssignmentResponse.model_validate(daily_assignment)

    async def delete_daily_assignment(
            self, daily_assignment_id: int
    ) -> schemas.SuccessResponse:
        daily_assignment = await self.crud.get(daily_assignment_id)
        if not daily_assignment:
            raise exceptions.ObjectNotFoundByIdError(
                "daily_assignment", daily_assignment_id
            )

        await self.crud.delete(daily_assignment_id)
        return schemas.SuccessResponse(success=True)
