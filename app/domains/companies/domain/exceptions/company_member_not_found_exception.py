"""Company member not found exception."""

from app.shared.exceptions import NotFoundException


class CompanyMemberNotFoundException(NotFoundException):
    """Raised when a membership lookup by company and user IDs returns no result.

    Args:
        user_id: The ULID of the user.
        company_id: The ULID of the company.
    """

    def __init__(self, user_id: str, company_id: str) -> None:
        """Initialise the exception with the missing membership pair.

        Args:
            user_id: The ULID of the user that is not a member.
            company_id: The ULID of the company.
        """
        super().__init__(
            message=f"User '{user_id}' is not a member of company '{company_id}'.",
            context={"user_id": user_id, "company_id": company_id},
            error_code="COMPANY_MEMBER_NOT_FOUND",
        )
