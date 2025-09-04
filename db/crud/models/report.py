from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

import exceptions
import schemas
from db.crud.models.base import BaseModelCrud
from db.models import DailyAssignment, InventoryUser, Location, Report, ReportRoom, User


class ReportCRUD(BaseModelCrud[Report]):
    model = Report
    user_model = User
    location_model = Location
    daily_assignment_model = DailyAssignment
    report_room_model = ReportRoom

    search_fields = ["message"]
    order_by = (
        "start_time", "end_time",
        "status", "daily_assignment_id",
        "user_id", "message", "media_links"
    )

    @staticmethod
    def build_report_response(report: Report) -> schemas.ReportResponse:
        report_rooms = [
            schemas.ReportRoomResponse.model_validate(rr, from_attributes=True)
            for rr in report.report_rooms or []
        ]

        return schemas.ReportResponse.model_validate(
            {
                "id": report.id,
                "daily_assignment_id": report.daily_assignment_id,
                "user_id": report.user_id,
                "location_name": (
                    report.daily_assignment.location.name
                    if report.daily_assignment and report.daily_assignment.location
                    else None
                ),
                "user_full_name": (
                    f"{report.user.full_name}"
                    if report.user else None
                ),
                "report_rooms": report_rooms,
                "message": report.message,
                "media_links": report.media_links,
                "status": report.status,
                "start_time": report.start_time,
                "end_time": report.end_time,
            }
        )

    @staticmethod
    def build_report_with_assignment_date_response(
            report: Report
    ) -> schemas.ReportWithAssignmentDateResponse:
        report_rooms = [
            schemas.ReportRoomResponse.model_validate(rr, from_attributes=True)
            for rr in report.report_rooms or []
        ]

        inventory_ending_titles = [
            iu.inventory.title for iu in report.inventory_users or []
        ]

        return schemas.ReportWithAssignmentDateResponse.model_validate(
            {
                "id": report.id,
                "daily_assignment_id": report.daily_assignment_id,
                "user_id": report.user_id,
                "location_name": (
                    report.daily_assignment.location.name
                    if report.daily_assignment and report.daily_assignment.location
                    else None
                ),
                "user_full_name": (
                    f"{report.user.full_name}"
                    if report.user else None
                ),
                "assignment_date": report.daily_assignment.date if
                report.daily_assignment else None,
                "report_rooms": report_rooms,
                "message": report.message,
                "media_links": report.media_links,
                "status": report.status,
                "start_time": report.start_time,
                "end_time": report.end_time,
                "inventory_ending_titles": inventory_ending_titles
            }
        )

    async def create_report(self, data: schemas.CreateReport) -> schemas.ReportResponse:
        try:
            report_data = data.model_dump(exclude={"report_rooms", "inventory_users"})
            report = Report(**report_data)

            self.db.add(report)
            await self.db.flush()

            report_rooms = []
            if data.report_rooms:
                for report_room in data.report_rooms:
                    report_room_obj = ReportRoom(
                        **report_room.model_dump(), report_id=report.id
                    )
                    report_rooms.append(report_room_obj)

                self.db.add_all(report_rooms)

            assignment = await self.db.get(DailyAssignment, report.daily_assignment_id)

            if assignment is None:
                raise exceptions.ObjectNotFoundByIdError(
                    "assignment", report.daily_assignment_id
                )

            report.status = data.status
            assignment.status = data.status

            if data.inventory_users is not None:
                inventory_users = []
                for inv_user in data.inventory_users:
                    inventory_user = InventoryUser(
                        report_id=report.id, **inv_user.model_dump()
                    )
                    inventory_users.append(inventory_user)

                self.db.add_all(inventory_users)

            await self.db.commit()
            report = await self.db.scalar(
                select(Report).options(
                    selectinload(Report.report_rooms), joinedload(Report.user),
                    joinedload(Report.daily_assignment).joinedload(
                        DailyAssignment.location
                    )
                ).where(
                    Report.id == report.id
                )
            )

            # return schemas.ReportResponse.model_validate(report, from_attributes=True)
            return self.build_report_response(report)

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise exceptions.ErrorDuringReportCreate({"error: ": e})

    # async def change_status(self, report_id: int, status: schemas.AssignmentStatus):
    #     report = await self.get(report_id)
    #     report.status = status
    #
    #     response = await self.db.execute(
    #         update(DailyAssignment)
    #         .where(
    #             DailyAssignment.id == report.daily_assignment_id
    #         )
    #         .values(status=status)
    #     )
    #     return schemas.ReportResponse.model_validate(report)
