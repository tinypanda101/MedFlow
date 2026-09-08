"""Application configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/medflow"
    secret_key: str
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env")

#without the .env file setting values, this line will raise an error on startup
settings = Settings()