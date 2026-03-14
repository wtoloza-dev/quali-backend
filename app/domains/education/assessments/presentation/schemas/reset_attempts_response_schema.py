"""Reset attempts response schema."""

from pydantic import BaseModel


class ResetAttemptsResponseSchema(BaseModel):
    """Response indicating how many attempts were deleted.

    Attributes:
        deleted_count: Number of attempts that were removed.
    """

    deleted_count: int
