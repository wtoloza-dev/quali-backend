"""Company SQLModel ORM model."""

import sqlalchemy as sa
from sqlmodel import Field

from app.shared.models import AuditModel

from ...domain.enums import CompanyType, Country, TaxType


class CompanyModel(AuditModel, table=True):
    """SQLModel ORM representation of the companies table.

    Maps the company data to the database. Used exclusively within
    the infrastructure layer — never returned directly to the application
    or presentation layers.

    Attributes:
        __tablename__: Database table name.
        name: Human-readable display name of the company.
        slug: URL-friendly unique identifier, indexed for fast lookups.
        company_type: Whether this is a personal or organization account.
        email: Primary contact email.
        country: Country where the company operates.
        legal_name: Official registered name, if different from display name.
        logo_url: URL of the company logo used on certificates.
        tax_type: Tax identifier type (NIT, CC). Stored flat alongside tax_id.
        tax_id: The actual tax identifier number.
    """

    __tablename__ = "companies"

    name: str = Field(nullable=False)
    slug: str = Field(nullable=False, unique=True, index=True)
    company_type: CompanyType = Field(sa_type=sa.String(), nullable=False)
    email: str = Field(nullable=False)
    country: Country = Field(sa_type=sa.String(), nullable=False)
    legal_name: str | None = Field(default=None, nullable=True)
    logo_url: str | None = Field(default=None, nullable=True)
    tax_type: TaxType | None = Field(default=None, sa_type=sa.String(), nullable=True)
    tax_id: str | None = Field(default=None, nullable=True)
