import httpx
from fastapi import HTTPException
from jose import JWTError
from starlette import status

import schemas
from config import settings
from db.crud import UserCRUD
from db.models import User
from utils.password import get_password_hash, verify_password
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

    async def forget_password(self, data: schemas.ForgetPasswordData):
        try:
            payload = decode_token(data.token)
            if payload.get("type") != "forget_password":
                raise JWTError()
            user_id = int(payload["sub"])
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired forget_password token: " + str(e)
            )

        user = await self.crud.get(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        hashed_password = get_password_hash(data.password)

        await self.crud.update(
            user, hashed_password=hashed_password
        )

        await self.crud.db.commit()

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

    async def request_access(
            self, data: schemas.RequestAccessCreate, parse_mode: str = "Markdown"
    ) -> schemas.SuccessResponse:

        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.CHAT_ID

        message = self.format_request_message(data.model_dump())

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode
        }

        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(telegram_url, json=payload)
                response.raise_for_status()
                return schemas.SuccessResponse(success=True)
            except httpx.HTTPError as e:
                raise Exception(f"Ошибка при отправке в телеграмм: {str(e)}")

    @staticmethod
    def format_request_message(data: dict) -> str:

        message = f"""
🆕 **Новый запрос на доступ**

👤 **Имя:** {data['full_name']}
📧 **Email:** {data['email']}
📞 **Телефон:** {data['phone_number']}
💬 **Сообщение:** {data.get('message', 'Не указано')}

        """.strip()

        return message
