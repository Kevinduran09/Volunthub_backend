from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    # APP
    APP_NAME: str = "Volunthub-backend"
    ENVIRONMENT: str = Field(default="development")

    # Server

    HOST: str = "0.0.0.0"
    PORT: str = 8000

    # database

    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
