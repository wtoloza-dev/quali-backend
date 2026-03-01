"""Test environment settings."""

from ._base_settings import BaseAppSettings


class TestSettings(BaseAppSettings):
    """Settings for the automated test environment.

    Overrides values that should differ during test runs, such as
    pointing to an in-memory or isolated test database.

    Attributes:
        DEBUG: Always True in test environment.
        SCOPE: Fixed to 'test'.
    """

    DEBUG: bool = True
    SCOPE: str = "test"
    DATABASE_URL: str = "postgresql+asyncpg://test:test@localhost:5432/test"
