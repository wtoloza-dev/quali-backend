"""get_company_by_id contract port.

Defines the minimal interface and return type for retrieving a company by ID
across domain boundaries. Any domain that needs to look up a company depends
only on this module — never on the companies domain directly.
"""

from typing import Protocol

from pydantic import BaseModel


class CompanyContractResult(BaseModel):
    """Minimal company projection returned by the get_company_by_id contract.

    Contains only the fields that cross-domain consumers are allowed to
    observe. Source-domain internals (audit fields, tax details, etc.)
    are not exposed.

    Attributes:
        id: ULID of the company.
        name: Human-readable display name.
        slug: URL-friendly unique identifier.
        logo_url: URL of the company logo, used on issued certificates.
    """

    id: str
    name: str
    slug: str
    logo_url: str | None


class GetCompanyByIdPort(Protocol):
    """Contract interface for fetching a company by ULID.

    Implemented by GetCompanyByIdAdapter in the infrastructure layer.
    Consumers (e.g. certification use cases) depend on this Protocol,
    making them testable with any fake that satisfies the interface.
    """

    async def __call__(self, company_id: str) -> CompanyContractResult | None:
        """Retrieve a company by its ULID.

        Args:
            company_id: ULID of the company to look up.

        Returns:
            CompanyContractResult if the company exists, None otherwise.
        """
        ...
