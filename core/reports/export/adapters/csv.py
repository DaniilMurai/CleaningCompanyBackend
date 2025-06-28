import csv
import io
from io import BytesIO

from fastapi import Depends

import schemas
from core.reports.export.adapters.base import ReportsAdapter
from db.crud.core.reports.export import ExportCrud


class CsvAdapter(ReportsAdapter):

    def __init__(
            self, params: schemas.ReportExportParams, crud: ExportCrud = Depends()
    ):
        super().__init__(params)
        self.crud = crud

    async def get_result(self) -> tuple[BytesIO, str]:
        data = await self.crud.get_reports_by_date(self.params)

        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(data[0].model_fields.keys())
        for row in data:
            writer.writerow(row.model_dump().values())

        byte_stream = io.BytesIO(stream.getvalue().encode("utf-8"))
        return byte_stream, "reports.csv"
