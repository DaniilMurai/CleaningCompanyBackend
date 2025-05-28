from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query

import schemas
from api.admin.router.locations.service import AdminLocationService

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/")
async def get_locations(
        params: Annotated[schemas.AdminGetListParams, Query()],
        service: AdminLocationService = Depends(),
) -> list[schemas.LocationResponse]:
    return await service.get_list(params)


@router.post("/")
async def create_location(
        data: schemas.LocationCreate,
        service: AdminLocationService = Depends(),
) -> schemas.LocationResponse:
    return await service.create(data)


@router.patch("/")
async def edit_location(
        location_id: int,
        data: schemas.LocationUpdate,
        service: AdminLocationService = Depends(),
) -> schemas.LocationResponse:
    return await service.update(location_id, data)


@router.delete("/")
async def delete_location(
        location_id: int,
        service: AdminLocationService = Depends()
) -> schemas.SuccessResponse:
    return await service.delete(location_id)
