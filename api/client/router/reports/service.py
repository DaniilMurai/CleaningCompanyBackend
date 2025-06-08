import exceptions
import schemas
from db.crud.models.report import ReportCRUD


class ReportService:
    def __init__(
            self,
            crud: ReportCRUD.depends()
    ):
        self.crud = crud

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

        report = await self.crud.update(report, data.model_dump(exclude_none=True))
        report = await self.crud.change_status(report.id, data.status)
        return schemas.ReportResponse.model_validate(report)
