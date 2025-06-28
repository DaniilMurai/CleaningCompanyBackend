from abc import ABC, abstractmethod
from io import BytesIO

import exceptions
import schemas


class ReportsAdapter(ABC):
    subclasses = {}

    def __init_subclass__(cls):
        class_name = cls.__name__.replace("Adapter", "").lower()
        cls.subclasses[class_name] = cls

    def __init__(self, params: schemas.ReportExportParams):
        self.params = params

    @classmethod
    async def execute(cls, params: schemas.ReportExportParams) -> tuple[BytesIO, str]:
        key = params.export_type.replace(" ", "").lower()
        print("Execute export_type:", params.export_type, "-> key:", key)
        for k in cls.subclasses.keys():
            print("Available adapters:", k)
        if key not in cls.subclasses:
            raise exceptions.IncorrectAdapterTypeValue(params.export_type)

        adapter = cls.subclasses[key](params)
        return await adapter.get_result()

    @abstractmethod
    async def get_result(self):
        raise NotImplementedError
