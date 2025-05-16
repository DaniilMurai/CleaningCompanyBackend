from fastapi import APIRouter, Depends

import schemas
from .service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/login")
async def login(
        data: schemas.LoginData,
        service: AuthService = Depends(),
) -> schemas.TokenPair:
    return await service.login(data)


@router.post("/activate")
async def activate(
        data: schemas.ActivateUserData,
        service: AuthService = Depends()
) -> schemas.TokenPair:
    return await service.activate(data)


@router.post("/refresh_tokens")
async def refresh_tokens(
        request: schemas.RefreshTokenData,
        service: AuthService = Depends()
) -> schemas.TokenPair:
    return await service.refresh_tokens(request)


@router.post("/forget-password")
async def forget_password(
        data: schemas.ForgetPasswordData,
        service: AuthService = Depends()
) -> schemas.TokenPair:
    return await service.forget_password(data)
