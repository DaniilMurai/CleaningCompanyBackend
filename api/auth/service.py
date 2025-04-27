from fastapi import HTTPException
from jose import JWTError
from starlette import status

import schemas
from db.crud import UserCRUD
from db.models import User
from utils.password import verify_password
from utils.security.tokens import (
    create_access_token, create_refresh_token,
    decode_token,
)


class AuthService:
    def __init__(self, crud: UserCRUD.depends()):
        self.crud = crud

    @classmethod
    def get_tokens_pair(cls, user: User):
        access = create_access_token(
            data={"sub": str(user.id), "type": "access"}
        )
        refresh = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})

        return schemas.TokenPair(access_token=access, refresh_token=refresh)

    async def login(self, data: schemas.LoginData):
        user = await self.crud.get(
            nickname=data.nickname,
            status=schemas.UserStatus.active
        )
        if (
                not user or
                (user and (not verify_password(data.password, user.hashed_password)))
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect nickname or password",
            )

        return self.get_tokens_pair(user)

    async def activate(self, data: schemas.ActivateUserData):
        try:
            payload = decode_token(data.token)
            if payload.get("type") != "invite":
                raise JWTError()
            user_id = int(payload["sub"])
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired invite token: " + str(e)
            )

        user = await self.crud.get(user_id)

        if not user or user.status != schemas.UserStatus.pending:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invite not found or already activated"
            )

        await self.crud.update(
            user, data.model_dump(exclude={"token"}, exclude_none=True),
            status=schemas.UserStatus.active
        )
        await self.crud.db.commit()

        return self.get_tokens_pair(user)

    async def refresh_tokens(self, request: schemas.RefreshTokenData):
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise JWTError()
        user_id = int(payload.get("sub"))

        user = await self.crud.get(user_id)
        if user.status != schemas.UserStatus.active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User status is not active"
            )

        return self.get_tokens_pair(user)
