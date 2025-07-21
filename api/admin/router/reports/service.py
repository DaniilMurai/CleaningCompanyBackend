import schemas
from api.admin.base.service import AdminGenericService
from db.crud.admin.report import AdminReportCRUD


class AdminReportService(
    AdminGenericService[
        schemas.CreateReport,
        schemas.UpdateReport,
        schemas.ReportResponse,
        schemas.AdminReportFilterParams,
        AdminReportCRUD
    ]
):
    response_schema = schemas.ReportResponse
    entity_name = "report"
    crud_cls = AdminReportCRUD

    async def get_reports(
            self, params: schemas.AdminReportFilterParams | None = None
    ) -> list[schemas.ReportWithAssignmentDateResponse]:
        return await self.crud.get_reports_crud(params)
