from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, HttpUrl, PostgresDsn, computed_field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.local"), env_file_encoding="utf-8")

    ENVIRONMENT: Literal["development", "production", "testing"] = "development"

    DEBUG: bool = False
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_PATH: str | None = None

    @property
    def is_debug(self) -> bool:
        return self.DEBUG or self.ENVIRONMENT in ("development", "testing")

    @property
    def openapi_url(self) -> str:
        if self.ENVIRONMENT != "development":
            return None
        else:
            return f"{settings.API_V1_STR}/openapi.json"

    BACKEND_EXT_PORT: int = 8000
    BACKEND_INT_PORT: int = 80

    PROJECT_NAME: str = "H2Optimize"
    DESCRIPTION: str = "Manage the rooms use"
    VERSION: str = "0.0.1"
    CONTACT_NAME: str = "H2Optimize"
    CONTACT_URL: HttpUrl = "https://github.com/h2optimize-end-of-study-project-hetic"
    CONTACT_EMAIL: EmailStr = "contact@hoptimize.fr"
    LICENCE_NAME: str = "MIT"
    API_V1_STR: str = "/api/v1"

    SERVERS: list = [
        {"url": f"http://localhost:{BACKEND_EXT_PORT}", "description": "Local development server"},
        {"url": "https://11.hetic.arcplex.dev:443", "description": "Production server"},
    ]

    FRONTEND_HOST: HttpUrl = "http://localhost:5173"

    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "app"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "Changeme!1"

    @computed_field
    @property
    def database_url(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
