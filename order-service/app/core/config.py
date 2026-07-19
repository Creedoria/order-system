"""Application settings loaded from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "order-service"
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/order-db"
    SECRET_KEY: str = "nakutelisindekoncham"
    ALGORITHM: str = "HS256"
    PAYMENT_SERVICE_URL: str = "http://localhost:8002"

    model_config = SettingsConfigDict(
        env_file=".env.development",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()