from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.locations.service import AdminLocationService

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/")
async def get_locations(
        params: Annotated[schemas.LocationUpdate, Query()],
        service: AdminLocationService = Depends(),
) -> list[schemas.LocationResponse]:
    return await service.get_locations(params)


@router.post("/")
async def create_location(
        data: schemas.LocationCreate,
        service: AdminLocationService = Depends(),
) -> schemas.LocationResponse:
    return await service.create_location(data)


@router.patch("/")
async def edit_location(
        location_id: int,
        data: schemas.LocationUpdate,
        service: AdminLocationService = Depends(),
) -> schemas.LocationResponse:
    return await service.update_location(location_id, data)


@router.delete("/")
async def delete_location(
        location_id: int,
        service: AdminLocationService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete_location(location_id)
