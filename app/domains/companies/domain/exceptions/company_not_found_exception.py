"""Company not found exception."""

from app.shared.exceptions import NotFoundException


class CompanyNotFoundException(NotFoundException):
    """Raised when a company lookup by ID returns no result.

    Args:
        company_id: The ULID that was not found.
    """

    def __init__(self, company_id: str) -> None:
        """Initialise the exception with the missing company ID.

        Args:
            company_id: The ULID of the company that was not found.
        """
        super().__init__(
            message=f"Company '{company_id}' not found.",
            context={"company_id": company_id},
            error_code="COMPANY_NOT_FOUND",
        )
