"""Base application settings."""

from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Shared configuration fields inherited by all environment settings.

    All concrete settings classes (LocalSettings, TestSettings, ProdSettings)
    extend this class. Values are loaded from environment variables automatically
    by pydantic-settings.

    Attributes:
        APP_NAME: Human-readable name of the application. Same across all envs.
        DEBUG: Whether debug mode is enabled. Must be set per environment.
        SCOPE: Active environment identifier (local, test, prod). Must be set per environment.
        DATABASE_URL: Async PostgreSQL DSN. Must be set per environment.
    """

    APP_NAME: str = "Quali API"
    DEBUG: bool
    SCOPE: str
    DATABASE_URL: str
    ENCRYPTION_KEY: str = ""
