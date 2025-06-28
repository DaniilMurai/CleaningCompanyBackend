from io import BytesIO

import schemas
from core.reports.export.adapters.base import ReportsAdapter
from .adapters.csv import CsvAdapter
from .adapters.excel import ExcelAdapter

excel = ExcelAdapter
csv = CsvAdapter


async def export_reports(params: schemas.ReportExportParams) -> tuple[BytesIO, str]:
    return await ReportsAdapter.execute(params)
