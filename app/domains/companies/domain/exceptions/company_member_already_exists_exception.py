"""Company member already exists exception."""

from app.shared.exceptions import ConflictException


class CompanyMemberAlreadyExistsException(ConflictException):
    """Raised when a user is already a member of the given company.

    Args:
        user_id: The ULID of the user.
        company_id: The ULID of the company.
    """

    def __init__(self, user_id: str, company_id: str) -> None:
        """Initialise the exception with the conflicting membership pair.

        Args:
            user_id: The ULID of the user that is already a member.
            company_id: The ULID of the company.
        """
        super().__init__(
            message=f"User '{user_id}' is already a member of company '{company_id}'.",
            context={"user_id": user_id, "company_id": company_id},
            error_code="COMPANY_MEMBER_ALREADY_EXISTS",
        )
