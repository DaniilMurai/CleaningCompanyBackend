from typing import Dict, Any

from fastapi import FastAPI
from fastapi.routing import APIRoute


class CustomFastApi(FastAPI):
    _is_route_operation_ids_set: bool = False

    def openapi(self) -> Dict[str, Any]:

        if not self._is_route_operation_ids_set:
            for route in self.routes:
                if isinstance(route, APIRoute):
                    route.operation_id = route.name
            self._is_route_operation_ids_set = True

        return super().openapi()
