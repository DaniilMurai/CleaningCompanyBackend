import asyncio
import os

import schemas
from api.admin.router.export_reports.service import AdminExportReportService
from db.crud.admin.export_report import AdminExportReportCRUD
from db.models import ReportsExport
from db.session import async_session_maker
from loggers import JSONLogger
from .functions import export_reports

SECONDS = 5

logger = JSONLogger('export_report_worker')

EXPORT_DIR = "app/data/export"


async def export_report_worker():
    logger.info("Export report worker started.")
    os.makedirs(EXPORT_DIR, exist_ok=True)
    while True:
        try:
            async with async_session_maker() as db:  # ✅ создаём сессию
                crud = AdminExportReportCRUD(db=db)
                service = AdminExportReportService(admin=None, crud=crud)

                report: ReportsExport | None = await service.get_next_waiting_report()
                logger.info("Export report worker in cycle.")
                if report:
                    logger.info(f"Found report ID={report.id}, marking as processing")
                    await service.set_export_report_status(
                        report, schemas.ReportStatus.in_progress
                    )

                    data = {
                        "export_type": report.export_type,
                        "start_date": report.start_date,
                        "end_date": report.end_date,
                        "user_id": report.user_id,
                    }
                    params = schemas.ReportExportParams.model_validate(data)
                    result = await export_reports(params)

                    if result and isinstance(result, tuple):
                        content, filename = result
                        file_path = os.path.join(EXPORT_DIR, f"/{report.id}_{filename}")

                        with open(file_path, "wb") as f:
                            f.write(content.getbuffer())

                        await service.set_export_report_status(
                            report, schemas.ReportStatus.completed, file_path=file_path
                        )
                        logger.info(
                            f"Report ID={report.id} exported successfully to "
                            f"{file_path}."
                        )
                    else:
                        logger.error(f"Report ID={report.id} export failed.")
                        await service.set_export_report_status(
                            report, schemas.ReportStatus.failed
                        )

        except Exception as e:
            logger.error(f"Unexpected error in export_report_worker: {str(e)}")

        await asyncio.sleep(SECONDS)
