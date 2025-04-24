from app.crud.admin.crud import AdminCRUD


class AdminService:
    def __init__(self, admin_crud: AdminCRUD):
        self.admin_crud = admin_crud

    async def get_users(
            self,
            search_by: str
            # user_id: Optional[UUID] = None,
            # nick_name: Optional[str] = None,
            # role: Optional[Role] = None,
            # full_name: Optional[str] = None,
            # description_from_admin: Optional[str] = None,
            # created_at: datetime = None,

    ):
        return await self.admin_crud.get_user()
