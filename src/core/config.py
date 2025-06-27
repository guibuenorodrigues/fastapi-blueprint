from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, Field, PlainValidator, computed_field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

from src.core.enums import EnvironmentEnum


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class ApplicationSettings(BaseSettings):
    """Application-specific settings, extending project settings and also reading from .env."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEV
    LOG_FORMAT: Literal["plaintext", "json"] = "json"
    LOG_LEVEL: Literal["CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    UVICORN_LOG_LEVEL: Literal["CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "WARNING"
    REQUEST_LOG_LEVEL: Literal["CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "INFO"
    ERROR_LOG_LEVEL: Literal["CRITICAL", "FATAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "ERROR"
    DATABASE_URL: str
    FRONTEND_HOST: str = "http://localhost:8000"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, PlainValidator(parse_cors)] = []

    @computed_field
    @property
    def allowed_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True, env_file=".env")


class ProjectSettings(ApplicationSettings):
    """Base settings for project metadata, loaded from pyproject.toml."""

    APP_NAME: str = Field(alias="name")
    APP_VERSION: str = Field(alias="version")
    APP_DESCRIPTION: str = Field(alias="description")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,  # Settings from constructor
            dotenv_settings,  # Settings from .env file
            env_settings,  # Settings from environment variables
            PyprojectTomlConfigSettingsSource(settings_cls, Path.cwd() / "pyproject.toml"),  # Settings from pyproject
            file_secret_settings,  # Settings from secrets files
        )

    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("project",),
        extra="ignore",
        case_sensitive=True,
        env_file=".env",  # Ensure .env is explicitly enabled for this model as well
    )


class Settings(ProjectSettings):
    pass


@lru_cache
def get_settings() -> Settings:
    """Return cached settings."""
    return Settings()


settings = get_settings()
