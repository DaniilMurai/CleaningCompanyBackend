from fastapi import APIRouter, Depends

import schemas
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
        data: schemas.LoginData,
        service: AuthService = Depends(),
) -> schemas.TokenPair:
    return await service.login(data)


@router.post("/activate")
async def activate(
        request: schemas.ActivateUserData,
        service: AuthService = Depends()
) -> schemas.TokenPair:
    return await service.activate(request)


@router.post("/refresh_tokens")
async def refresh_tokens(
        request: schemas.RefreshTokenData,
        service: AuthService = Depends()
) -> schemas.TokenPair:
    return await service.refresh_tokens(request)
