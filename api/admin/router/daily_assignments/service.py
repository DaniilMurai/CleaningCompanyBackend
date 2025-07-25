from sqlalchemy import func, select

import exceptions
import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.daily_assignment import AdminDailyAssignmentCRUD
from db.models import DailyAssignment


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

    async def get_daily_assignments(
            self, params: schemas.AdminAssignmentDatesGetListParams | None = None
    ) -> list[schemas.DailyAssignmentWithLocationAndUserResponse]:
        dates = params.dates if params.dates else None
        assignments = await self.crud.get_daily_assignments(dates)
        return [schemas.DailyAssignmentWithLocationAndUserResponse.model_validate(a) for
                a in
                assignments]

    async def create_daily_assignments_batch(
            self, data: list[schemas.DailyAssignmentCreate]
    ) -> list[schemas.DailyAssignmentResponse]:
        return await self.crud.create_daily_assignments_batch(data)

    async def get_daily_assignments_dates(self):
        assignment_dates = await self.crud.db.execute(
            select(

                func.date(DailyAssignment.date),

            ).distinct().where(DailyAssignment.is_deleted == False)
            .order_by(func.date(DailyAssignment.date))
        )
        return assignment_dates.scalars().all()

    async def check_assignment_group(
            self, daily_assignments_id: int
    ) -> schemas.AssignmentGroup:
        return await self.crud.check_assignment_group(daily_assignments_id)

    async def delete_daily_assignments_group(
            self, daily_assignments_id: int
    ) -> schemas.SuccessResponse:
        assignment = await self.crud.get(daily_assignments_id)
        if not assignment:
            raise exceptions.ObjectNotFoundByIdError("assignment", daily_assignments_id)
        await self.crud.delete_daily_assignments_group(assignment)
        return schemas.SuccessResponse(success=True)
