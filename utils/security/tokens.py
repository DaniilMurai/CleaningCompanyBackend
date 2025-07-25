from typing import Optional

from asyncpg.pgproto.pgproto import timedelta
from jose import JWTError, jwt

from config import settings
from utils.date_time import utcnow

SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRES = timedelta(minutes=45)
REFRESH_TOKEN_EXPIRES = timedelta(days=14)
INVITE_TOKEN_EXPIRES = timedelta(days=14)
ALGORITHM = settings.ALGORITHM

token_blacklist = set()


def decode_token(token: str):
    if token in token_blacklist:
        raise JWTError("Token revoked")
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise JWTError(f"Invalid token: {e}")


def create_invite_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # sub должна быть строка, потом нужно будет переводить в инт если буду работать с
    # базой
    to_encode["sub"] = str(to_encode["sub"])

    if expires_delta:
        expire = utcnow() + expires_delta
    else:
        expire = utcnow() + INVITE_TOKEN_EXPIRES

    to_encode.update({"exp": expire, "type": "invite"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_forget_password_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # sub должна быть строка, потом нужно будет переводить в инт если буду работать с
    # базой
    to_encode["sub"] = str(to_encode["sub"])

    if expires_delta:
        expire = utcnow() + expires_delta
    else:
        expire = utcnow() + INVITE_TOKEN_EXPIRES

    to_encode.update({"exp": expire, "type": "forget_password"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # sub должна быть строка, потом нужно будет переводить в инт если буду работать с
    # базой
    to_encode["sub"] = str(to_encode["sub"])

    if expires_delta:
        expire = utcnow() + expires_delta
    else:
        expire = utcnow() + ACCESS_TOKEN_EXPIRES

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # sub должна быть строка, потом нужно будет переводить в инт если буду работать с
    # базой
    to_encode["sub"] = str(to_encode["sub"])

    if expires_delta:
        expire = utcnow() + expires_delta
    else:
        expire = utcnow() + REFRESH_TOKEN_EXPIRES

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
