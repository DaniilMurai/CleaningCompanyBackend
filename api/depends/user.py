import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
from starlette import status

import schemas
from db.crud import UserCRUD
from .token import get_token_data


async def get_current_user(
        scopes: SecurityScopes,
        token_data: Annotated[dict, Depends(get_token_data("access"))],
        crud: Annotated[UserCRUD, Depends()],
):
    try:
        user_id = int(token_data["sub"])
    except Exception as e:
        logging.error(f"Paring token sub error: {repr(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e

    user = await crud.get(user_id, status=schemas.UserStatus.active)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    for scope in scopes.scopes:
        if scope not in user.allowed_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    return user
