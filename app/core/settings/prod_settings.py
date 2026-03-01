"""Production settings."""

from ._base_settings import BaseAppSettings


class ProdSettings(BaseAppSettings):
    """Settings for the production environment.

    Enforces strict, secure defaults. Debug is always disabled.
    All sensitive values must be provided via environment variables.

    Attributes:
        DEBUG: Always False in production.
        SCOPE: Fixed to 'prod'.
    """

    DEBUG: bool = False
    SCOPE: str = "prod"
