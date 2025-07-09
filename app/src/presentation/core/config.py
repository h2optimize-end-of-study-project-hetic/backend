import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str = "H2Optimize"
    DESCRIPTION: str = "Manage the rooms use"
    VERSION: str = "0.0.1"
    CONTACT_NAME: str = "H2Optimize" 
    CONTACT_EMAIL: str = "contact@hoptimize.fr"
    LICENCE_NAME: str = "MIT"
    API_V1_STR: str = "/api/v1"

    FRONTEND_HOST: str = "http://localhost:5173"
    


settings = Settings()