from db.crud.models.base import BaseModelCrud
from db.models import Room


class RoomCRUD(BaseModelCrud[Room]):
    model = Room
    search_fields = "name"
