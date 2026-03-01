"""Company domain entity."""

from pydantic import BaseModel

from app.shared.entities import AuditEntity

from ..enums import CompanyType, Country
from ..value_objects import Tax


class CompanyData(BaseModel):
    """Lean company data used by use cases that create a company.

    Attributes:
        name: Human-readable display name of the company.
        slug: URL-friendly unique identifier derived from the name.
        company_type: Whether this is a personal (unipersonal) or full organization.
        email: Primary contact email for the company.
        country: Country where the company operates (ISO 3166-1 alpha-2).
        tax: Tax identification value object (type + id). Optional.
        legal_name: Official registered name, if different from display name.
        logo_url: URL of the company logo, shown on issued certificates.
    """

    name: str
    slug: str
    company_type: CompanyType
    email: str  # TODO: add validation for email or use email type from pydantic
    country: Country
    tax: Tax | None = None
    legal_name: str | None = None
    logo_url: str | None = None


class CompanyEntity(CompanyData, AuditEntity):
    """Full company entity returned by the repository after persistence.

    Combines the domain fields from CompanyData with the audit fields
    from AuditEntity. Use cases receive CompanyData as input and
    CompanyEntity as output from the repository.
    """

    pass
