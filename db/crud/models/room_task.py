from db.crud.models.base import BaseModelCrud
from db.models import RoomTask


class RoomTaskCRUD(BaseModelCrud[RoomTask]):
    model = RoomTask
    # search_fields = ["task_id", "room_id", "times_since_done"]
