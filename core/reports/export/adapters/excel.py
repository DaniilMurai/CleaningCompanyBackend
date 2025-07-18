from io import BytesIO

import pandas as pd

from core.reports.export.adapters.base import ReportsAdapter


class ExcelAdapter(ReportsAdapter):

    async def get_result(self, data) -> tuple[BytesIO, str]:
        rows = [{k: v for k, v in row.items() if not k.startswith("_")} for row
                in data]
        df = pd.DataFrame(rows)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for col in df.select_dtypes(include=["datetimetz"]).columns:
                df[col] = df[col].dt.tz_localize(None)

            df.to_excel(writer, index=False, engine="openpyxl")

        output.seek(0)
        return output, "xlsx"
