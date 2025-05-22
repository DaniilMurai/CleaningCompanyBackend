import exceptions
import schemas
from db.crud.admin.location import AdminLocationsCRUD
from schemas import LocationUpdate


class AdminLocationService:

    def __init__(
            self,
            crud: AdminLocationsCRUD.depends()
    ):
        self.crud: AdminLocationsCRUD = crud

    async def get_locations(self, params: LocationUpdate | None = None) -> list[
        schemas.LocationResponse]:
        kwargs = params.model_dump(exclude_none=True) if params else {}
        locations = await self.crud.get_list(**kwargs)
        return [schemas.LocationResponse.model_validate(loc) for loc in locations]

    async def create_location(
            self, data: schemas.LocationCreate
    ) -> schemas.LocationResponse:
        location = await self.crud.create(**data.model_dump(exclude_none=True))
        return schemas.LocationResponse.model_validate(location)

    async def update_location(
            self, location_id: int, data: schemas.LocationUpdate
    ) -> schemas.LocationResponse:
        location = await self.crud.get(location_id)

        if not location:
            raise exceptions.ObjectNotFoundByIdError("location", location_id)

        date_to_update = data.model_dump(exclude_none=True)
        location = await self.crud.update(location, date_to_update)

        return schemas.LocationResponse.model_validate(location)

    async def delete_location(self, location_id):
        await self.crud.delete(location_id)
        return schemas.SuccessResponse(success=True)
