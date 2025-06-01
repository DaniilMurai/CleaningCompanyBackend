from db.crud.models.base import BaseModelCrud
from db.models import Task


class TaskCRUD(BaseModelCrud[Task]):
    model = Task
    search_fields = "name"
