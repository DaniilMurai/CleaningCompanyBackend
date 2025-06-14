from sqlalchemy import update

import schemas
from db.crud.models.base import BaseModelCrud
from db.models import DailyAssignment, Report


class ReportCRUD(BaseModelCrud[Report]):
    model = Report
    search_fields = ["message"]
    order_by = (
        "start_time", "end_time",
        "status", "daily_assignment_id",
        "user_id", "message", "media_links"
    )

    async def change_status(self, report_id: int, status: schemas.AssignmentStatus):
        report = await self.get(report_id)
        report.status = status

        response = await self.db.execute(
            update(DailyAssignment)
            .where(
                DailyAssignment.id == report.daily_assignment_id
            )
            .values(status=status)
        )
        return schemas.ReportResponse.model_validate(report)
