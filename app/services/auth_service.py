from fastapi import HTTPException
from jose import JWTError
from starlette import status

from app.crud.auth.crud import AuthCRUD
from app.models.User.model import UserStatus
from app.schemas.auth.ActivateRequest import ActivateRequest
from app.schemas.auth.TokenPair import RefreshRequest, TokenPair
from app.security.tokens import create_access_token, create_refresh_token, decode_token
from app.utils.password.functions import verify_password


class AuthService:
    def __init__(self, auth_crud: AuthCRUD):
        self.auth_crud = auth_crud

    async def activate(self, request: ActivateRequest):
        try:
            payload = decode_token(request.token)
            if payload.get("type") != "invite":
                raise JWTError()
            user_id = int(payload["sub"])
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired invite token: " + str(e)
            )

        user = await self.auth_crud.get_user_by_id(user_id)

        if not user or user.status != UserStatus.pending:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invite not found or already activated"
            )

        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong password"
            )

        user.status = UserStatus.active
        await self.auth_crud.db.commit()

        access = create_access_token(
            data={"sub": str(user.id), "role": user.role.value, "type": "access"}
        )
        refresh = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})

        return TokenPair(access_token=access, refresh_token=refresh)

    async def refresh_tokens(self, request: RefreshRequest):
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise JWTError()
        user_id = int(payload.get("sub"))

        user = await self.auth_crud.get_user_by_id(user_id)
        if user.status != UserStatus.active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User status is not active"
            )

        access = create_access_token(
            data={"sub": str(user.id), "role": user.role.value, "type": "access"}
        )
        refresh = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})

        return TokenPair(access_token=access, refresh_token=refresh)
