from db.crud.models.base import BaseModelCrud
from db.models import InventoryUser


class InventoryUserCRUD(BaseModelCrud[InventoryUser]):
    model = InventoryUser
