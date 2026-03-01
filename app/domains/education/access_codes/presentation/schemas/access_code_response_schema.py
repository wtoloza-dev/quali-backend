"""Access code response schema."""

from datetime import datetime

from pydantic import BaseModel


class AccessCodeResponseSchema(BaseModel):
    """Full access code response for authenticated users.

    Attributes:
        id: ULID of the access code.
        code: The access code string (QUALI-XXXX-XXXX format).
        course_id: ULID of the course this code unlocks.
        company_id: ULID of the company (tenant scope).
        is_redeemed: Whether this code has been used.
        redeemed_by: ULID of the user who redeemed the code.
        redeemed_at: Timestamp when the code was redeemed.
        created_at: Audit timestamp.
        created_by: ULID of the creator.
        updated_at: Audit timestamp.
        updated_by: ULID of the last updater.
    """

    id: str
    code: str
    course_id: str
    company_id: str
    is_redeemed: bool
    redeemed_by: str | None
    redeemed_at: datetime | None
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
