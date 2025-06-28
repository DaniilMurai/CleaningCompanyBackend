from typing import Sequence

from sqlalchemy import CursorResult, Result, and_, func, select
from sqlalchemy.exc import SQLAlchemyError

import schemas
from db.crud.models.export_report import ExportReportCRUD
from db.models import Report, ReportsExport
from loggers import JSONLogger

logger = JSONLogger("export_report")


class AdminExportReportCRUD(ExportReportCRUD):
    # model = Report
    # user_model = User
    # location_model = Location
    # daily_assignment_model = DailyAssignment
    #
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
