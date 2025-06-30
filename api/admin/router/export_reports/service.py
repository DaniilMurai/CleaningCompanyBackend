import os.path

from starlette.responses import FileResponse

import exceptions
import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.export_report import AdminExportReportCRUD
from db.models import ReportsExport
from schemas import ReportStatus


class AdminExportReportService(
    AdminGenericService[
        schemas.ReportExportParams,
        schemas.ReportExportParams,
        schemas.ReportExportResponse,
        schemas.AdminReportFilterParams,
        AdminExportReportCRUD
    ]
):
    response_schema = schemas.ReportExportResponse
    entity_name = "export_report"
    crud_cls = AdminExportReportCRUD

    async def export_reports(self, params: schemas.ReportExportParams) -> int:
        export_report = await self.crud.create(params.model_dump(exclude_none=True))

        return export_report.id

    async def get_next_waiting_report(self):
        return await self.crud.get_next_waiting_report()

    async def set_export_report_status(
            self, report: ReportsExport, status: ReportStatus,
            file_path: str | None = None
    ):
        return await self.crud.set_report_status(report, status, file_path)

    async def download_report(self, export_id: int) -> FileResponse:
        export = await self.crud.get(export_id)
        if export.status == schemas.ReportStatus.failed:
            raise exceptions.ReportExportStatusFailed
        if export.status != schemas.ReportStatus.completed:
            raise exceptions.ReportExportIsNotCompletedYet

        print("export.file_path: ", export.file_path)

        if not os.path.exists(export.file_path):
            raise exceptions.ReportExportIsNotCompletedYet

        media_type = ""
        for char in export.file_path[::-1]:
            if char == ".":
                break
            media_type += char
        media_type = media_type[::-1]

        print("media_type: ", media_type)

        return FileResponse(
            path=export.file_path, media_type=f"text/{media_type}",
            filename=f"report_{export_id}.{media_type}"
        )
