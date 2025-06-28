from db.crud.models.base import BaseModelCrud
from db.models import ReportsExport


class ExportReportCRUD(BaseModelCrud[ReportsExport]):
    model = ReportsExport
