from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    FRONTEND_URL: str
    HOST: str = "localhost"
    PORT: int = 8000
    RELOAD: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
