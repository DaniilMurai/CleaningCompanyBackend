from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_and_generate_hash(
        new_password: str,
        current_hashed_password: str | None = None
):
    if current_hashed_password and verify_password(
            new_password, current_hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can't change the password to the one you have"
        )

    return get_password_hash(new_password)
