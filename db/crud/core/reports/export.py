from db.crud.base import CRUD
from db.models import DailyAssignment, Location, Report, User


class ExportCrud(CRUD):
    model = Report
    user_model = User
    location_model = Location
    daily_assignment_model = DailyAssignment

    # async def get_reports_by_date(self, params: schemas.ReportExportParams) -> list[
    #     schemas.ReportExportRow]:
    #     conditions = [
    #         func.date(self.model.start_time) >= params.start_date,
    #         func.date(self.model.end_time) <= params.end_date
    #     ]
    #
    #     if params.user_id:
    #         conditions.append(self.model.user_id == params.user_id)
    #
    #     stmt = (
    #         select(
    #             self.model.id,
    #             self.model.start_time,
    #             self.model.end_time,
    #             self.model.status,
    #             self.model.message,
    #             self.user_model.full_name.label("user_full_name"),
    #             self.location_model.name.label("location_name"),
    #             self.location_model.address.label("location_address"),
    #             self.daily_assignment_model.date.label("assignment_date")
    #         )
    #         .join(self.user_model, self.model.user_id == self.user_model.id)
    #         .join(
    #             self.daily_assignment_model,
    #             self.model.daily_assignment_id == self.daily_assignment_model.id
    #         )
    #         .join(
    #             self.location_model,
    #             self.daily_assignment_model.location_id == self.location_model.id
    #         )
    #         .where(and_(*conditions))
    #         .order_by(self.model.id)
    #     )
    #
    #     result = await self.db.execute(stmt)
    #     rows = result.all()
    #
    #     return [schemas.ReportExportRow.model_validate(r) for r in rows]
