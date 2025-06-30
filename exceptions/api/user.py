from starlette import status

import schemas
from .base import APIException


class NicknameCannotBeEmptyError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Nickname cannot be empty"


class NicknameAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, nickname: str):
        self.message = f"User with nickname {nickname} already exists."
        self.nickname = nickname
        self.data = {"nickname": nickname}


class CreateUserWithRoleForbiddenError(APIException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, role: schemas.UserRole):
        self.message = f"You cannot create user with role: {role.value}"
        self.role = role
        self.data = {"role": role.value}


class WrongPasswordError(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, password: str):
        self.message = f"Password {password} is not correct."
        self.password = password
        self.data = {"password": password}


class UserAlreadyActivated(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, role: schemas.UserRole):
        self.message = f"User with {role} role already activated"
        self.role = role
        self.data = {"role": role}
