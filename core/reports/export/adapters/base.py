from abc import ABC, abstractmethod
from io import BytesIO

import exceptions
import schemas
from db.crud.admin.export_report import AdminExportReportCRUD


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
        return await self.crud.get_reports_by_date(self.params)

    async def run(self):
        data = await self.get_data()
        return await self.get_result(data)

    @abstractmethod
    async def get_result(self, data):
        raise NotImplementedError
