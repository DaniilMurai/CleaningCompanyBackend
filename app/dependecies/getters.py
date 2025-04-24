from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.admin.crud import AdminCRUD
from app.db.dependencies import get_db
from app.services.admin_service import AdminService


async def get_admin_service(
        db: AsyncSession = Depends(get_db)
) -> AdminService:
    admin_crud = AdminCRUD(db)
    return AdminService(admin_crud)
