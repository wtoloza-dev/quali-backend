"""Update company request schema."""

from pydantic import BaseModel

from ...domain.enums import CompanyType, Country, TaxType


class TaxRequestSchema(BaseModel):
    """Tax identification input for create and update requests.

    Attributes:
        tax_type: The type of tax identifier.
        tax_id: The actual tax identifier number.
    """

    tax_type: TaxType
    tax_id: str


class UpdateCompanyRequestSchema(BaseModel):
    """Input schema for the update company endpoint.

    All fields are optional — only provided fields will be updated.
    Slug is intentionally excluded: it is immutable once set.

    Attributes:
        name: New display name for the company.
        company_type: New company type classification.
        email: New primary contact email.
        country: New country.
        tax: New tax identification.
        legal_name: New official registered name.
        logo_url: New logo URL.
    """

    name: str | None = None
    company_type: CompanyType | None = None
    email: str | None = None
    country: Country | None = None
    tax: TaxRequestSchema | None = None
    legal_name: str | None = None
    logo_url: str | None = None
