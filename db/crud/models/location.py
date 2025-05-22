from db.crud.models.base import BaseModelCrud
from db.models import Location


class LocationCRUD(BaseModelCrud[Location]):
    model = Location
    search_fields = ("name", "address")
