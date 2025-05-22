from db.crud.admin.room_task import AdminRoomTaskCRUD


class AdminRoomTaskService:
    def __init__(
            self,
            crud: AdminRoomTaskCRUD.depends()
    ):
        self.crud: AdminRoomTaskCRUD = crud
