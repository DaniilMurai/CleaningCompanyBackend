from api.custom_fastapi import CustomFastApi
from .router import router
from ..base.exception_handlers import register_general_exception_handlers

app = CustomFastApi(title="Neuer Standart Client API")

app.include_router(router=router)

register_general_exception_handlers(app)
