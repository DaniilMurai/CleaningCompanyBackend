from abc import ABC, abstractmethod
from io import BytesIO

import exceptions
import schemas
from db.crud.admin.export_report import AdminExportReportCRUD
from utils.date_time import format_duration
from utils.init_i18n import locale_export_reports


class ReportsAdapter(ABC):
    subclasses = {}

    def __init_subclass__(cls):
        class_name = cls.__name__.replace("Adapter", "").lower()
        cls.subclasses[class_name] = cls

    def __init__(self, params: schemas.ReportExportParams, crud: AdminExportReportCRUD):
        self.params = params
        self.crud = crud

    @classmethod
    async def execute(
            cls, params: schemas.ReportExportParams, crud: AdminExportReportCRUD
    ) -> tuple[BytesIO, str]:
        key = params.export_type.replace(" ", "").lower()
        print("Execute export_type:", params.export_type, "-> key:", key)
        for k in cls.subclasses.keys():
            print("Available adapters:", k)
        if key not in cls.subclasses:
            raise exceptions.IncorrectAdapterTypeValue(params.export_type)

        return await cls.subclasses[key](params, crud).run()

    async def get_data(self):
        data = await self.crud.get_reports_by_date(self.params)
        locale = self.params.lang
        rows = []
        for row in data:
            row_dict = row.model_dump()
            row_dict.pop('start_time', None)
            row_dict.pop('end_time', None)
            row_dict = {
                "id": row.id,
                "location_name": row.location_name,
                "user_full_name": row.user_full_name,
                "start_time_str": row.start_time_str,
                "end_time_str": row.end_time_str,
                "duration": format_duration(row.duration()),
                "status": row.status,
                "message": row.message
            }

            rows.append(locale_export_reports(row_dict, locale))
        return rows

    async def run(self):
        data = await self.get_data()
        return await self.get_result(data)

    @abstractmethod
    async def get_result(self, data):
        raise NotImplementedError
