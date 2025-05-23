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

    class Config:
        env_file = ".env"


settings = Settings()
