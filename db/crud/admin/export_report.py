from sqlalchemy import CursorResult, Result, Sequence, and_, func, select
from sqlalchemy.exc import SQLAlchemyError

import schemas
from db.crud.models.export_report import ExportReportCRUD
from db.models import Report, ReportsExport
from loggers import JSONLogger

logger = JSONLogger("export_report")


class AdminExportReportCRUD(ExportReportCRUD):

    async def get_next_waiting_report(self) -> CursorResult | Result | None:
        try:
            report = await self.db.execute(
                select(ReportsExport)
                .where(
                    ReportsExport.status == schemas.ReportStatus.waiting
                )
                .order_by(ReportsExport.id.asc())
                .limit(1)
            )
            return report.scalars().one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Failed to fetch next waiting export task from DB: {e}")
            return None

    async def set_report_status(
            self, export_report: ReportsExport, status: schemas.ReportStatus,
            file_path: str | None = None
    ):
        if file_path:
            return await self.update(
                export_report, {"status": status, "file_path": file_path}
            )
        else:
            return await self.update(export_report, {"status": status})

    async def get_reports_by_date(self, params: schemas.ReportExportParams) -> \
            Sequence[Report]:

        conditions = [
            func.date(Report.start_time) >= params.start_date,
            func.date(Report.end_time) <= params.end_date
        ]

        if params.user_id:
            conditions.append(Report.user_id == params.user_id)

        reports = await self.db.execute(select(Report).where(and_(*conditions)))

        return reports.scalars().all()
