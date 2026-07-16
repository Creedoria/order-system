"""Application settings loaded from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "users-service"
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3308/users_db"

    model_config = SettingsConfigDict(
        env_file=".env.development",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()