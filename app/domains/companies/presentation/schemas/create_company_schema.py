"""Create company request schema."""

from pydantic import BaseModel

from ...domain.enums import CompanyType, Country
from .update_company_schema import TaxRequestSchema


class CreateCompanyRequestSchema(BaseModel):
    """Input schema for the create company endpoint.

    Validates and deserializes the HTTP request body for company
    registration. Only exposes fields that the API consumer is allowed
    to provide.

    Attributes:
        name: Human-readable display name of the company.
        slug: URL-friendly unique identifier.
        company_type: Whether this is a personal or organization account.
        email: Primary contact email.
        country: Country where the company operates.
        tax: Tax identification. Optional.
        legal_name: Official registered name, if different from display name.
        logo_url: URL of the company logo.
    """

    name: str
    slug: str
    company_type: CompanyType
    email: str
    country: Country
    tax: TaxRequestSchema | None = None
    legal_name: str | None = None
    logo_url: str | None = None
