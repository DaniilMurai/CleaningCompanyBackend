from sqlalchemy import and_, or_, select
from sqlalchemy.orm import joinedload, selectinload

import schemas
from db.crud.models.report import ReportCRUD


class AdminReportCRUD(ReportCRUD):

    async def get_reports_crud(
            self, params: schemas.AdminReportFilterParams | None = None,
    ) -> list[schemas.ReportWithAssignmentDateResponse]:

        conditions = []
        if params.status:
            conditions.append(self.model.status == params.status)

        if params.search:
            conditions.append(
                or_(
                    self.model.message.ilike(f"%{params.search}%"),
                    self.user_model.full_name.ilike(f"%{params.search}%"),
                    self.location_model.name.ilike(f"%{params.search}%"),
                    self.location_model.address.ilike(f"%{params.search}%"),
                )
            )

        stmt = select(self.model).where(
            and_(*conditions, self.model.is_deleted == False)
        ).join(
            self.user_model, self.model.user_id == self.user_model.id,
        ).join(
            self.daily_assignment_model,
            self.model.daily_assignment_id == self.daily_assignment_model.id
        ).join(
            self.location_model,
            self.daily_assignment_model.location_id == self.location_model.id
        ).options(
            selectinload(self.model.report_rooms),
            joinedload(self.model.user),
            joinedload(self.model.daily_assignment).joinedload(
                self.daily_assignment_model.location
            )
        )

        if params.order_by:
            field = params.order_by
            order = getattr(self.model, field)
            if params.direction == "asc":
                stmt = stmt.order_by(order.asc())
            else:
                stmt = stmt.order_by(order.desc())
        else:
            stmt = stmt.order_by(self.model.id.desc())

        stmt = await self.paginate(stmt, params.offset, params.limit)

        result = await self.db.scalars(stmt)
        return [self.build_report_with_assignment_date_response(r) for r in
                result.all()]
