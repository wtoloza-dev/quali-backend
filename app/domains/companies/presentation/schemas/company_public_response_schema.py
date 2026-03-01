"""Company public response schema."""

from pydantic import BaseModel

from ...domain.enums import CompanyType, Country


class CompanyPublicResponseSchema(BaseModel):
    """Public-facing company data safe to expose without authentication.

    Excludes PII fields such as email and tax identification.
    Used in contexts like certificate verification pages where the
    issuing company is shown to anonymous users.

    Attributes:
        id: ULID of the company.
        name: Human-readable display name.
        slug: URL-friendly unique identifier.
        company_type: Personal or organization.
        country: Country where the company operates.
        legal_name: Official registered name, if available.
        logo_url: URL of the company logo, if available.
    """

    id: str
    name: str
    slug: str
    company_type: CompanyType
    country: Country
    legal_name: str | None
    logo_url: str | None
