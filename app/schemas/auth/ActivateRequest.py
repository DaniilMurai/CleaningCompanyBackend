from pydantic import BaseModel


class ActivateRequest(BaseModel):
    token: str
    password: str
