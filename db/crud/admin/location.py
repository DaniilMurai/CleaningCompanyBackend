from sqlalchemy import select

from db.crud.models.location import LocationCRUD
from db.models import Location


class AdminLocationsCRUD(LocationCRUD):

    async def get_locations(self):
        locations = await self.db.execute(select(Location))
        return locations.scalars().all()
