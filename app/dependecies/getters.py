from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.admin.crud import AdminCRUD
from app.crud.auth.crud import AuthCRUD
from app.db.dependencies import get_db
from app.services.admin_service import AdminService
from app.services.auth_service import AuthService


async def get_admin_service(
        db: AsyncSession = Depends(get_db)
) -> AdminService:
    admin_crud = AdminCRUD(db)
    return AdminService(admin_crud)


async def get_auth_service(
        db: AsyncSession = Depends(get_db)
) -> AuthService:
    auth_crud = AuthCRUD(db)
    return AuthService(auth_crud)
