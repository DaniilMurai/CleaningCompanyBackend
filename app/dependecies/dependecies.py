from fastapi import Depends

from app.db.dependencies import get_db
from app.dependecies.getters import get_admin_service, get_auth_service

DataBaseDependency = Depends(get_db)
AdminServiceDependency = Depends(get_admin_service)
AuthServiceDependency = Depends(get_auth_service)
