import schemas
from db.crud.models.base import BaseModelCrud
from db.models import DailyAssignment, Report


class DailyAssignmentCRUD(BaseModelCrud[DailyAssignment]):
    model = DailyAssignment
    search_fields = ("admin_note")
    report_model = Report

    async def get_assignment_and_reports(
            self, assignments: list[schemas.DailyAssignmentForUserResponse]
    ) -> list[schemas.AssignmentReportResponse]:
        assignment_ids = []
        for a in assignments:
            assignment_ids.append(a.id)

        reports = await self.get_list(
            model=self.report_model, ids=assignment_ids, f="daily_assignment_id"
        )

        reports_map = {r.daily_assignment_id: r for r in reports}
        assignments_reports = []
        for a in assignments:
            report = reports_map.get(a.id)
            assignments_reports.append({"assignment": a, "report": report})

        assignments_reports = [schemas.AssignmentReportResponse.model_validate(
            assignment_report
        ) for assignment_report in assignments_reports]

        return assignments_reports
