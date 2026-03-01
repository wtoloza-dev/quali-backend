"""Company slug taken exception."""

from app.shared.exceptions import ConflictException


class CompanySlugTakenException(ConflictException):
    """Raised when a company with the given slug already exists.

    Args:
        slug: The slug that caused the conflict.
    """

    def __init__(self, slug: str) -> None:
        """Initialise the exception with the conflicting slug.

        Args:
            slug: The slug that is already taken.
        """
        super().__init__(
            message=f"A company with slug '{slug}' already exists.",
            context={"slug": slug},
            error_code="COMPANY_SLUG_TAKEN",
        )
