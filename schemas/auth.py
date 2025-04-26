from typing import Literal

from pydantic import BaseModel, ConfigDict


class LoginData(BaseModel):
    nickname: str
    password: str


class ActivateUserData(BaseModel):
    token: str
    password: str


class TokenPair(BaseModel):
    model_config = ConfigDict(
        json_schema_serialization_defaults_required=True
    )

    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"


class RefreshTokenData(BaseModel):
    refresh_token: str
