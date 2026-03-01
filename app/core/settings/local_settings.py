"""Local development settings."""

from pydantic_settings import SettingsConfigDict

from ._base_settings import BaseAppSettings


class LocalSettings(BaseAppSettings):
    """Settings for local development.

    Enables debug mode and relaxed configuration suitable for
    running the application on a developer machine. Reads from a
    .env file in the project root if present.

    Attributes:
        DEBUG: Always True in local environment.
        SCOPE: Fixed to 'local'.
        DATABASE_URL: Points to local Docker PostgreSQL instance.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DEBUG: bool = True
    SCOPE: str = "local"
    DATABASE_URL: str = "postgresql+asyncpg://quali:quali@localhost:5432/quali"
