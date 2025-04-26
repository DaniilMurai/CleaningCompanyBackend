from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from starlette import status

from utils.security.tokens import decode_token

http_bearer_scheme = HTTPBearer()


def get_token(
        data: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer_scheme)]
):
    return data.credentials


def get_token_data(token_type: str | None = None):
    def depend(
            token: Annotated[str, Depends(get_token)]
    ):
        try:
            payload = decode_token(token)
            if payload.get("type") != token_type:
                raise JWTError()
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            ) from e

    return depend
