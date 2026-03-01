"""get_company_member contract port.

Defines the minimal interface and return type for retrieving a company
member across domain boundaries. Used by the shared require_role guard
so it never imports directly from the companies domain.
"""

from typing import Protocol

from pydantic import BaseModel


class CompanyMemberContractResult(BaseModel):
    """Minimal company member projection returned by the contract.

    Attributes:
        company_id: ULID of the company.
        user_id: ULID of the user.
        role: The member's role value as a string.
    """

    company_id: str
    user_id: str
    role: str


class GetCompanyMemberPort(Protocol):
    """Contract interface for fetching a company member."""

    async def __call__(
        self, company_id: str, user_id: str
    ) -> CompanyMemberContractResult | None:
        """Retrieve a company member by company and user IDs.

        Args:
            company_id: ULID of the company.
            user_id: ULID of the user.

        Returns:
            CompanyMemberContractResult if found, None otherwise.
        """
        ...
