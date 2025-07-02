from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

import exceptions
import schemas
from db.crud.models.base import BaseModelCrud
from db.models import DailyAssignment, Location, Report, ReportRoom, User


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

    async def create_report(self, data: schemas.CreateReport) -> schemas.ReportResponse:
        try:
            report_data = data.model_dump(exclude={"report_rooms"})
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

            await self.db.commit()
            report = await self.db.scalar(
                select(Report).options(selectinload(Report.report_rooms)).where(
                    Report.id == report.id
                )
            )
            return schemas.ReportResponse.model_validate(report, from_attributes=True)

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise exceptions.ErrorDuringReportCreate({"error: ": e})

    async def change_status(self, report_id: int, status: schemas.AssignmentStatus):
        report = await self.get(report_id)
        report.status = status

        response = await self.db.execute(
            update(DailyAssignment)
            .where(
                DailyAssignment.id == report.daily_assignment_id
            )
            .values(status=status)
        )
        return schemas.ReportResponse.model_validate(report)
