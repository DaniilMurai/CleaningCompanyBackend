from sqlalchemy import select

from db.crud.models.report import ReportCRUD
from db.models import Report


class AdminReportCRUD(ReportCRUD):

    async def get_reports(self):
        reports = await self.db.execute(select(Report))
        return reports.scalars().all()
