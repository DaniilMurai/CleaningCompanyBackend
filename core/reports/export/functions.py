from io import BytesIO

import schemas
from db.crud.admin.export_report import AdminExportReportCRUD
from .adapters import ReportsAdapter


# excel = ExcelAdapter
# csv = CsvAdapter


async def export_reports(
        params: schemas.ReportExportParams, crud: AdminExportReportCRUD
) -> tuple[BytesIO, str]:
    return await ReportsAdapter.execute(params, crud)
