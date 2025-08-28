from db.crud.models.base import BaseModelCrud
from db.models import Hint


class HintCRUD(BaseModelCrud[Hint]):
    model = Hint
    search_fields = ["text"]
