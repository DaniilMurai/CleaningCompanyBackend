from fastapi import APIRouter

from app.dependecies.dependecies import AuthServiceDependency
from app.schemas.auth.ActivateRequest import ActivateRequest
from app.schemas.auth.TokenPair import RefreshRequest, TokenPair
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login():
    pass


@router.post("/activate", response_model=TokenPair)
async def activate(
        request: ActivateRequest,
        auth_service: AuthService = AuthServiceDependency
):
    return await auth_service.activate(request)


@router.post("/refresh_tokens")
async def refresh_tokens(
        request: RefreshRequest,
        auth_service: AuthService = AuthServiceDependency
):
    return await auth_service.refresh_tokens(request)
