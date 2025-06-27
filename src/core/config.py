from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)


class ApplicationSettings(BaseSettings):
    """Application-specific settings, extending project settings and also reading from .env."""

    DEBUG: bool = False
    DATABASE_URL: str

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True, env_file=".env")


class ProjectSettings(ApplicationSettings):
    """Base settings for project metadata, loaded from pyproject.toml."""

    NAME: str = Field(alias="name")
    VERSION: str = Field(alias="version")
    DESCRIPTION: str = Field(alias="description")

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


print("chamaaaa", Settings())
settings = get_settings()
