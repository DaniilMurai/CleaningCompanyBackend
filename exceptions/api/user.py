from starlette import status

from exceptions.api.base import APIException


class NicknameCannotBeEmptyError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Nickname cannot be empty"


class NicknameAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, nickname: str):
        self.message = f"User with nickname {nickname} already exists."
        self.nickname = nickname
        self.data = {"nickname": nickname}
