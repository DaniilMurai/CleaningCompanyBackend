import json
import os.path

from fastapi.responses import FileResponse, StreamingResponse

import exceptions
import loggers
import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.export_report import AdminExportReportCRUD
from db.models import ReportsExport
from redis_client import redis
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
        if not await self.crud.check_if_reports_exists(params):
            raise exceptions.ObjectsNotFoundByIdsError("reports for user(s)", [])

        export_report = await self.crud.create(params.model_dump(exclude_unset=True))

        return export_report.id

    async def get_next_waiting_report(self):
        return await self.crud.get_next_waiting_report()

    async def set_export_report_status(
            self, report: ReportsExport, status: ReportStatus,
            file_path: str | None = None
    ):
        return await self.crud.set_report_status(report, status, file_path)

    async def get_export_type(self, export_id: int) -> schemas.FileResponse:
        export = await self.crud.get(export_id)
        if not export:
            raise exceptions.ObjectNotFoundByIdError("export_report", export_id)
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
        return schemas.FileResponse(
            path=export.file_path, media_type=f"text/{media_type}",
            filename=f"report_{export_id}.{media_type}"
        )

    async def download_report(self, export_id: int) -> FileResponse:
        obj = await self.get_export_type(export_id)
        return FileResponse(
            path=obj.path, media_type=obj.media_type,
            filename=obj.filename
        )

    @staticmethod
    async def stream_export_reports():
        pubsub = redis.pubsub()
        await pubsub.subscribe("export_report")
        logger = loggers.JSONLogger("stream_export_reports")

        async def event_generator():
            try:
                async for message in pubsub.listen():
                    if message['type'] == "message":
                        data = json.dumps(message)
                        logger.info(data)
                        yield f"data: {data}\n\n"
            except Exception as e:
                logger.error("An error occurred while handling redis messages: ", e)
            finally:
                await redis.aclose()

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    async def get_export_reports(
            self, params: schemas.AdminGetListParams | None = None
    ) -> list[schemas.ReportExportResponse]:
        export_reports = await self.crud.get_export_reports(params)

        return [schemas.ReportExportResponse(
            id=report.id,
            status=report.status,
            export_type=report.export_type,
            start_date=report.start_date,
            end_date=report.end_date,
            timezone=report.timezone,
            lang=report.lang,
            user_full_name=report.user.full_name if report.user else None

        ) for report in export_reports]
