"""Access code not found exception."""

from app.shared.exceptions import NotFoundException


class AccessCodeNotFoundException(NotFoundException):
    """Raised when an access code cannot be found.

    Args:
        code: The access code string that was not found.
    """

    def __init__(self, code: str) -> None:
        """Initialise with the missing access code.

        Args:
            code: The access code string that was not found.
        """
        super().__init__(
            message=f"Access code '{code}' not found.",
            context={"code": code},
            error_code="ACCESS_CODE_NOT_FOUND",
        )
