"""Country enum."""

from enum import StrEnum


class Country(StrEnum):
    """Supported countries using ISO 3166-1 alpha-2 codes.

    Expand this enum as new markets are supported.
    """

    CO = "CO"
