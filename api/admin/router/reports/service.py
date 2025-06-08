import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.report import AdminReportCRUD


class AdminReportService(
    AdminGenericService[
        schemas.CreateReport,
        schemas.UpdateReport,
        schemas.ReportResponse,
        schemas.AdminGetListParams,
        AdminReportCRUD
    ]
):
    response_schema = schemas.ReportResponse
    entity_name = "report"
    crud_cls = AdminReportCRUD
