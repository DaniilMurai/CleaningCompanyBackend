from db.crud.models.base import BaseModelCrud
from db.models import Inventory


class InventoryCRUD(BaseModelCrud[Inventory]):
    search_fields = ("title", "description")
    model = Inventory
