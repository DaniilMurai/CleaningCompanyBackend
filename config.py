import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    FRONTEND_URL: str
    HOST: str
    PORT: int = 8000
    RELOAD: bool = False
    DEFAULT_LANG: str = "en"
    LOGS_DIR: str = "logs"
    LOGGER_NAME: str = "neuer-standard"
    LOCALES_PATH: str = "locales"
    OUTPUT_REPORTS_EXPORTS_DIR: str = os.path.join(os.getcwd(), "exports")

    class Config:
        env_file = ".env"


settings = Settings()
