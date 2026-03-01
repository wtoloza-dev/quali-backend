"""Settings singleton for the Quali API.

Resolves the correct settings class based on the SCOPE environment
variable and exposes a single `settings` instance used across the application.

Usage:
    from app.core.settings import settings

    print(settings.APP_NAME)
"""

import os

from ._base_settings import BaseAppSettings
from .local_settings import LocalSettings
from .prod_settings import ProdSettings
from .test_settings import TestSettings


_SETTINGS_MAP: dict[str, type[BaseAppSettings]] = {
    "local": LocalSettings,
    "test": TestSettings,
    "prod": ProdSettings,
}


def get_settings() -> BaseAppSettings:
    """Resolve and instantiate the correct settings class for the active environment.

    Reads the SCOPE environment variable to determine which settings
    class to instantiate. Defaults to LocalSettings when SCOPE is
    not set.

    Returns:
        BaseAppSettings: A fully initialised settings instance for the
        active environment.

    Raises:
        ValueError: If SCOPE is set to an unrecognised value.
    """
    env = os.getenv("SCOPE", "local")

    if env not in _SETTINGS_MAP:
        raise ValueError(
            f"Unknown SCOPE '{env}'. Valid values: {', '.join(_SETTINGS_MAP)}."
        )

    return _SETTINGS_MAP[env]()


settings: BaseAppSettings = get_settings()
