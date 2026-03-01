"""Tax type enum."""

from enum import StrEnum


class TaxType(StrEnum):
    """Supported tax identifier types per country.

    Expand this enum as new countries are supported.

    Values:
        NIT: Número de Identificación Tributaria (Colombia) — used by organizations.
        CC: Cédula de Ciudadanía (Colombia) — used by personal/unipersonal entities.
    """

    NIT = "NIT"
    CC = "CC"
