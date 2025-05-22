from sqlalchemy import select

from db.crud.models.room import RoomCRUD
from db.models import Room


class AdminRoomCRUD(RoomCRUD):

    async def get_rooms(self):
        rooms = await self.db.execute(select(Room))
        return rooms.scalars().all()
