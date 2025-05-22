from sqlalchemy import select

from db.crud.models.room_task import RoomTaskCRUD
from db.models import RoomTask


class AdminRoomTaskCRUD(RoomTaskCRUD):

    async def get_room_tasks(self):
        room_tasks = await self.db.execute(select(RoomTask))
        return room_tasks.scalars().all()
