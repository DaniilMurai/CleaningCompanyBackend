import csv
import io
from io import BytesIO

from core.reports.export.adapters.base import ReportsAdapter


class CsvAdapter(ReportsAdapter):

    async def get_result(self, data) -> tuple[BytesIO, str]:
        if not data:
            raise ValueError("Нет данных для экспорта")

        stream = io.StringIO()
        writer = csv.writer(stream)

        first_row = {k: v for k, v in data[0].__dict__.items() if not k.startswith("_")}
        writer.writerow(first_row.keys())

        for row in data:
            row_dict = {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
            writer.writerow(row_dict.values())

        byte_stream = io.BytesIO(stream.getvalue().encode("utf-8"))
        return byte_stream, "reports.csv"
