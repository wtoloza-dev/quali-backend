"""Company type enum."""

from enum import StrEnum


class CompanyType(StrEnum):
    """Represents whether a company is a full organization or a single person.

    A personal company is a unipersonal entity where one individual acts
    as both the owner and the certificate issuer.
    """

    PERSONAL = "personal"
    ORGANIZATION = "organization"
