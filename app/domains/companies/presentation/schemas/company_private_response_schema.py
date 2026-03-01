"""Company private response schema."""

from pydantic import BaseModel

from ...domain.enums import CompanyType, Country, TaxType


class TaxResponseSchema(BaseModel):
    """Serialized tax identification data.

    Attributes:
        tax_type: The type of tax identifier.
        tax_id: The actual tax identifier number.
    """

    tax_type: TaxType
    tax_id: str


class CompanyPrivateResponseSchema(BaseModel):
    """Full company data returned only to authenticated company members.

    Includes PII fields such as email and tax identification that must
    not be exposed to anonymous users.

    Attributes:
        id: ULID of the company.
        name: Human-readable display name.
        slug: URL-friendly unique identifier.
        company_type: Personal or organization.
        email: Primary contact email.
        country: Country where the company operates.
        tax: Tax identification, if provided.
        legal_name: Official registered name, if available.
        logo_url: URL of the company logo, if available.
    """

    id: str
    name: str
    slug: str
    company_type: CompanyType
    email: str
    country: Country
    tax: TaxResponseSchema | None
    legal_name: str | None
    logo_url: str | None
