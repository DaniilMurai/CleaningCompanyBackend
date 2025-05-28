from typing import Annotated, TypeVar

from fastapi.params import Security

import schemas
from api.depends.user import get_current_user
from db.models import User

T = TypeVar("T")

AdminUserDepend = Annotated[
    User, Security(
        get_current_user,
        scopes=[schemas.UserRole.admin.value]
    )
]
