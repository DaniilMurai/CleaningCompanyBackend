import exceptions
import schemas
from db.crud.models.report import ReportCRUD


class ReportService:
    def __init__(
            self,
            crud: ReportCRUD.depends()
    ):
        self.crud = crud

    async def get_reports_by_assignment_ids(self, assignment_ids: list[int]) -> list[
        schemas.ReportResponse]:

        reports = await self.crud.get_list(ids=assignment_ids, f="daily_assignment_id")

        if not reports:
            raise exceptions.ObjectsNotFoundByIdsError(
                "report assignment_id", assignment_ids
            )

        return [schemas.ReportResponse.model_validate(report) for report in reports]

    async def create_report(self, data: schemas.CreateReport) -> schemas.ReportResponse:
        report = await self.crud.create(data.model_dump())
        report = await self.crud.change_status(
            report.id, data.status
        )  # status in_progress
        return schemas.ReportResponse.model_validate(report)

    async def update_report(
            self, report_id: int, data: schemas.UpdateReport
    ) -> schemas.ReportResponse:
        report = await self.crud.get(report_id)

        if not report:
            raise exceptions.ObjectNotFoundByIdError("report", report_id)

        report = await self.crud.update(report, data.model_dump(exclude_unset=True))
        report = await self.crud.change_status(report.id, data.status)
        return schemas.ReportResponse.model_validate(report)
