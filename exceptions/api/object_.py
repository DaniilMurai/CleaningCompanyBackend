from starlette import status

from .base import APIException


class ObjectNotFoundByIdError(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, obj_name: str, id: int):
        self.message = f"{obj_name} not found by id {id}"
        self.data = {"obj_name": obj_name, "id": id}


class ObjectsNotFoundByIdsError(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, obj_name: str, ids: list[int]):
        self.message = f"{obj_name} not found by id {ids}"
        self.data = {"obj_name": obj_name, "id": ids}
