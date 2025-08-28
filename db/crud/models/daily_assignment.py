from sqlalchemy import select
from sqlalchemy.orm import selectinload

import schemas
from db.crud.models.base import BaseModelCrud
from db.models import DailyAssignment, Report


class DailyAssignmentCRUD(BaseModelCrud[DailyAssignment]):
    model = DailyAssignment
    search_fields = ("admin_note")
    report_model = Report

    async def get_assignment_and_reports(
            self, assignments: list[schemas.DailyAssignmentForUserWithHintsResponse]
    ) -> list[schemas.AssignmentWithHintsReportResponse]:
        assignment_ids = []
        for a in assignments:
            assignment_ids.append(a.id)

        if not assignment_ids:
            return []

        reports = (
            await self.db.execute(
                select(Report)
                .options(selectinload(Report.report_rooms))
                .where(
                    Report.daily_assignment_id.in_(assignment_ids)
                )
            )
        ).scalars().all()

        reports_map = {r.daily_assignment_id: r for r in reports}
        assignments_reports = []
        for a in assignments:
            assignments_reports.append(
                {"assignment": a, "report": reports_map.get(a.id)}
            )

        assignments_reports = [schemas.AssignmentWithHintsReportResponse.model_validate(
            assignment_report, from_attributes=True
        ) for assignment_report in assignments_reports]

        return assignments_reports
