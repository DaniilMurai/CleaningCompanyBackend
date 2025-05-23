from db.crud.models.base import BaseModelCrud
from db.models import DailyAssignment


class DailyAssignmentCRUD(BaseModelCrud[DailyAssignment]):
    model = DailyAssignment
    search_fields = ("id", "date", "admin_note", "user_id", "location_id")
