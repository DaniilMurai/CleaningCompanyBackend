from datetime import datetime, timezone

import i18n
from dateutil.tz import tz
from pydantic import ValidationError
from pytz import utc
from sqlalchemy import CursorResult, Result, and_, desc, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

import schemas
from db.crud.models.export_report import ExportReportCRUD
from db.models import (
    DailyAssignment, Location, Report, ReportRoom, ReportsExport,
    Room, User,
)
from loggers import JSONLogger
from utils.init_i18n import locale_str

logger = JSONLogger("export_report")


def convert_time(row: dict, time_zone: str):
    for key in ["start_time", "end_time"]:
        dt = row[key]
        if dt is not None:
            row[key] = dt.astimezone(time_zone)
    return row


def localise_datetime(
        dt: datetime, to_time_zone: str, from_timezone: str = None
) -> datetime:  # timezone may be utc
    if not isinstance(dt, datetime):
        print("not isinstance: ", type(dt))
        return dt
    from_timezone = timezone(from_timezone) if from_timezone else utc
    to_time_zone = tz.gettz(to_time_zone) if to_time_zone != "utc" else tz.tzutc()
    if not dt.tzinfo:
        dt = from_timezone.localize(dt)
    dt = dt.astimezone(to_time_zone)
    return dt


class AdminExportReportCRUD(ExportReportCRUD):
    user_model = User
    location_model = Location
    daily_assignment_model = DailyAssignment

    async def get_reports_by_date(self, params: schemas.ReportExportParams) -> list[
        schemas.ReportExportRow]:
        conditions = [
            func.date(Report.start_time) >= params.start_date,
            func.date(Report.end_time) <= params.end_date,
            Report.is_deleted == False
        ]

        if params.user_id:
            conditions.append(Report.user_id == params.user_id)

        stmt = (
            select(
                Report.id,
                Report.start_time,
                Report.end_time,
                Report.status,
                Report.message,
                self.user_model.full_name.label("user_full_name"),
                self.location_model.name.label("location_name"),
                self.location_model.address.label("location_address"),
                func.date(self.daily_assignment_model.date).label("assignment_date"),
                func.array_agg(Room.name).label("rooms"),
                func.array_agg(ReportRoom.status).label("room_statuses")
                # <- здесь именно список имён
            )
            .join(self.user_model, Report.user_id == self.user_model.id)
            .join(
                self.daily_assignment_model,
                Report.daily_assignment_id == self.daily_assignment_model.id
            )
            .join(
                self.location_model,
                self.daily_assignment_model.location_id == self.location_model.id
            )
            .outerjoin(ReportRoom, ReportRoom.report_id == Report.id)
            .outerjoin(
                Room,
                and_(
                    ReportRoom.room_id == Room.id,
                    ReportRoom.status != schemas.RoomStatus.done
                )
            )
            .where(and_(*conditions))
            .group_by(
                Report.id,
                Report.start_time,
                Report.end_time,
                Report.status,
                Report.message,
                self.user_model.full_name,
                self.location_model.name,
                self.location_model.address,
                func.date(self.daily_assignment_model.date)
            )
            .order_by(Report.id)
        )

        result = await self.db.execute(stmt)
        rows = result.mappings().all()

        processed_rows = []
        partially: str = locale_str(i18n.t("partially"), params.lang)
        for r in rows:
            row_dict = dict(r)
            if row_dict.get("rooms") is None:
                row_dict["rooms"] = []
            else:
                rooms_with_status = []
                for room, room_status in zip(
                        row_dict["rooms"], row_dict["room_statuses"]
                ):
                    if room is None:
                        continue
                    if room_status == schemas.RoomStatus.partially_done:
                        rooms_with_status.append(f"{room} {partially}")
                    else:
                        rooms_with_status.append(room)

                row_dict["rooms"] = rooms_with_status

                # row_dict["rooms"] = [room for room in row_dict["rooms"]
                #                      if room is not None]

            processed_rows.append(row_dict)
            processed_rows[-1]["start_time"] = localise_datetime(
                r.start_time, params.timezone
            )
            processed_rows[-1]["end_time"] = localise_datetime(
                r.end_time, params.timezone
            )
        valid_rows = []
        for r in processed_rows:
            try:
                valid_rows.append(schemas.ReportExportRow.model_validate(r))
                print(f"Validating report ID={r['id']}")
            except ValidationError as e:
                print(f"Skipping report ID={r['id']}: {e}")

        return valid_rows

    async def get_export_reports(
            self, params: schemas.AdminGetListParams | None = None
    ):
        stmt = (
            select(self.model)
            .where(self.model.is_deleted == False)
            .order_by(desc(self.model.id))
            .options(
                joinedload(self.model.user)
            ))

        stmt = await self.paginate(stmt, params.offset, params.limit)
        stmt = await self.db.execute(stmt)
        return stmt.scalars().all()

    async def get_next_waiting_report(self) -> CursorResult | Result | None:
        try:
            report = await self.db.execute(
                select(self.model)
                .where(
                    and_(
                        self.model.status == schemas.ReportStatus.waiting,
                        self.model.is_deleted == False
                    )
                )
                .order_by(self.model.id.asc())
                .limit(1)
            )
            return report.scalars().one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Failed to fetch next waiting export task from DB: {e}")
            return None

    async def set_report_status(
            self, export_report: ReportsExport, status: schemas.ReportStatus,
            file_path: str | None = None
    ):
        if file_path:
            return await self.update(
                export_report, {"status": status, "file_path": file_path}
            )
        else:
            return await self.update(export_report, {"status": status})
