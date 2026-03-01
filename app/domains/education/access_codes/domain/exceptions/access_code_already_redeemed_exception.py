"""Access code already redeemed exception."""

from app.shared.exceptions import ConflictException


class AccessCodeAlreadyRedeemedException(ConflictException):
    """Raised when an access code has already been redeemed.

    Args:
        code: The access code string that was already redeemed.
    """

    def __init__(self, code: str) -> None:
        """Initialise with the already-redeemed access code.

        Args:
            code: The access code string that was already redeemed.
        """
        super().__init__(
            message=f"Access code '{code}' has already been redeemed.",
            context={"code": code},
            error_code="ACCESS_CODE_ALREADY_REDEEMED",
        )
