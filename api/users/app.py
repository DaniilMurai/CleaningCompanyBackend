from .router import router
from ..base.exception_handlers import register_general_exception_handlers
from ..custom_fastapi import CustomFastApi

app = CustomFastApi(
    title="Neuer Standard Users API",
)
register_general_exception_handlers(app)

app.include_router(router)
