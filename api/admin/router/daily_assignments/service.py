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

    async def get_daily_assignments(
            self, params: schemas.AdminAssignmentDatesGetListParams | None = None
    ) -> list[schemas.DailyAssignmentResponse]:
        dates = params.dates if params.dates else None
        assignments = await self.crud.get_daily_assignments(dates)
        return [schemas.DailyAssignmentResponse.model_validate(a) for a in assignments]
