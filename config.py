import os

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    FRONTEND_URL: str
    HOST: str
    PORT: int = 8000
    RELOAD: bool = False
    WORKERS: int = 1
    DEFAULT_LANG: str = "en"
    LOGS_DIR: str = "logs"
    LOGGER_NAME: str = "neuer-standard"
    LOCALES_PATH: str = "locales"
    OUTPUT_REPORTS_EXPORTS_DIR: str = os.path.join(os.getcwd(), "exports")
    IMAGES_DIR: str = os.path.join(os.getcwd(), "images")
    IMAGES_HINTS_DIR: str = os.path.join(IMAGES_DIR, "hints")
    IMAGES_REPORTS_DIR: str = os.path.join(IMAGES_DIR, "reports")
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    BASE_URL: str = "http://192.168.178.39:8000"


settings = Settings()
