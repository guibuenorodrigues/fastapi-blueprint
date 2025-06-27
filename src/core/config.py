from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Application Settings."""

    DEBUG: bool = False
    DATABASE_URL: str

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True)


class ProjectSettings(Settings):
    """Application Settings."""

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
        return (PyprojectTomlConfigSettingsSource(settings_cls, Path.cwd() / "pyproject.toml"),)

    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("project",),
    )


@lru_cache
def get_settings() -> ProjectSettings:
    """Return cached settings."""
    return ProjectSettings()


settings = ProjectSettings()
