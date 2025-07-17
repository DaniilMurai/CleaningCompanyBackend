from sqlalchemy import func, select

import exceptions
import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.daily_assignment import AdminDailyAssignmentCRUD
from db.models import DailyAssignment
from schemas import DailyAssignmentResponse


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
    ) -> list[schemas.DailyAssignmentResponse]:
        dates = params.dates if params.dates else None
        assignments = await self.crud.get_daily_assignments(dates)
        return [schemas.DailyAssignmentResponse.model_validate(a) for a in assignments]

    async def get_daily_assignments_dates(self):
        assignment_dates = await self.crud.db.execute(
            select(

                func.date(DailyAssignment.date),

            ).distinct().where(DailyAssignment.is_deleted == False)
            .order_by(func.date(DailyAssignment.date))
        )
        return assignment_dates.scalars().all()

    async def check_assignment_group(self, daily_assignments_id: int) -> list[
        DailyAssignmentResponse]:
        assignments = await self.crud.check_assignment_group(daily_assignments_id)
        return [schemas.DailyAssignmentResponse.model_validate(assignment) for
                assignment in assignments]

    async def delete_daily_assignments_group(
            self, daily_assignments_id: int
    ) -> schemas.SuccessResponse:
        assignment = await self.crud.get(daily_assignments_id)
        if not assignment:
            raise exceptions.ObjectNotFoundByIdError("assignment", daily_assignments_id)
        await self.crud.delete_daily_assignments_group(assignment.group_uuid)
        return schemas.SuccessResponse(success=True)
