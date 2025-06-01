from db.crud.models.base import BaseModelCrud
from db.models import DailyAssignment


class DailyAssignmentCRUD(BaseModelCrud[DailyAssignment]):
    model = DailyAssignment
    search_fields = ("admin_note")
