from io import BytesIO

import pandas as pd
from fastapi.params import Depends

import schemas
from core.reports.export.adapters.base import ReportsAdapter
from db.crud.core.reports.export import ExportCrud


class ExcelAdapter(ReportsAdapter):

    def __init__(
            self, params: schemas.ReportExportParams, crud: ExportCrud = Depends()
    ):
        super().__init__(params)
        self.crud = crud

    async def get_result(self) -> tuple[BytesIO, str]:
        reports = await self.crud.get_reports_by_date(self.params)
        df = pd.DataFrame([r.model_dump() for r in reports])
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        output.seek(0)
        return output, "reports.xlsx"
