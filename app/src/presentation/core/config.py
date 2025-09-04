from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, HttpUrl, PostgresDsn, computed_field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.local"), env_file_encoding="utf-8")


    # General
    ENVIRONMENT: Literal["development", "production", "testing"] = "development"

    DEBUG: bool = False
    LOG_LEVEL: str = "DEBUG"

    BACKEND_EXT_PORT: int = 8000
    BACKEND_INT_PORT: int = 80  
    API_PREFIX: str = ""
    API_V1_STR: str = "/api/v1"

    LOG_FILE_PATH: str | None = None

    FRONTEND_HOST: HttpUrl = "http://localhost:5173"

    # Security 
    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def is_debug(self) -> bool:
        return self.DEBUG or self.ENVIRONMENT in ("development", "testing")


    # External APIs
    OPENWEATHER_API_KEY: str | None = None
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"
    

    # OpenAPI
    @property
    def openapi_url(self) -> str:
        if self.ENVIRONMENT == "development":
            return "/openapi.json"
        else:
            return "/openapi.json"
 
    SERVERS: list = [
        {"url": f"http://localhost:{BACKEND_EXT_PORT}", "description": "Local dev"},
        {"url": "https://11.hetic.arcplex.dev/release_back", "description": "Release server"}
    ]

    PROJECT_NAME: str = "H2Optimize"
    DESCRIPTION: str = "Manage the rooms use"
    VERSION: str = "0.0.2"
    CONTACT_NAME: str = "H2Optimize"
    CONTACT_URL: HttpUrl = "https://github.com/h2optimize-end-of-study-project-hetic"
    CONTACT_EMAIL: EmailStr = "contact@hoptimize.fr"
    LICENCE_NAME: str = "MIT"
    
    # DATABASE
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "Changeme!1"
    POSTGRES_DB: str = "app"
    POSTGRES_DB_RECORDED: str = "recorded"

    @computed_field
    @property
    def database_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
        ))
    
    @computed_field
    @property
    def database_recorded_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB_RECORDED,
        ))


settings = Settings()
