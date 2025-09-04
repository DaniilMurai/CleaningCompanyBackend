import exceptions
import schemas
from db.crud.models.report import ReportCRUD
from utils.image_files import convert_base64_to_server_link


class ReportService:
    def __init__(
            self,
            crud: ReportCRUD.depends()
    ):
        self.crud = crud

    async def get_reports_by_assignment_ids(self, assignment_ids: list[int]) -> list[
        schemas.ReportResponse]:

        reports = await self.crud.get_list(ids=assignment_ids, f="daily_assignment_id")

        if not reports:
            raise exceptions.ObjectsNotFoundByIdsError(
                "report assignment_id", assignment_ids
            )

        return [schemas.ReportResponse.model_validate(report) for report in reports]

    async def create_report(self, data: schemas.CreateReport) -> schemas.ReportResponse:

        if not data.media_links:
            return await self.crud.create_report(data)

        file_urls = await convert_base64_to_server_link(data.media_links, 'reports')

        report = data.model_copy(update={'media_links': file_urls})
        # schemas.CreateReport(
        #     **data.model_dump(), media_links=file_urls
        # )

        return await self.crud.create_report(report)

    # async def update_report(
    #         self, report_id: int, data: schemas.UpdateReport
    # ) -> schemas.ReportResponse:
    #     report = await self.crud.get(report_id)
    #
    #     if not report:
    #         raise exceptions.ObjectNotFoundByIdError("report", report_id)
    #
    #     updated_data = data.model_dump(exclude_unset=True)
    #
    #     if data.media_links:
    #         new_files = set(
    #             await convert_base64_to_server_link(data.media_links, 'reports')
    #         )
    #         old_files = set(report.media_links)
    #         for old_file in old_files - new_files:
    #             filename = old_file.split('/')[-1]
    #             file_path = os.path.join(settings.IMAGES_REPORTS_DIR, filename)
    #             if os.path.exists(file_path):
    #                 os.remove(file_path)
    #         updated_data['media_links'] = new_files
    #
    #     report = await self.crud.update(report, updated_data)
    #     report = await self.crud.change_status(report.id, data.status)
    #     return schemas.ReportResponse.model_validate(report)
