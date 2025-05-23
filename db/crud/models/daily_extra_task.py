from db.crud.models.base import BaseModelCrud
from db.models import DailyExtraTask


class DailyExtraTaskCRUD(BaseModelCrud[DailyExtraTask]):
    model = DailyExtraTask
    search_fields = ("daily_assignment_id", "room_id", "task_id")
