"""Access code domain entity."""

from datetime import datetime

from pydantic import BaseModel

from app.shared.entities import AuditEntity


class AccessCodeData(BaseModel):
    """Input fields required to create an access code.

    Attributes:
        code: Unique access code string (QUALI-XXXX-XXXX format).
        course_id: ULID of the course this code unlocks.
        company_id: ULID of the company (tenant scope).
    """

    code: str
    course_id: str
    company_id: str


class AccessCodeEntity(AccessCodeData, AuditEntity):
    """Full persisted access code record.

    Attributes:
        is_redeemed: Whether this code has been used.
        redeemed_by: ULID of the user who redeemed the code.
        redeemed_at: Timestamp when the code was redeemed.
    """

    is_redeemed: bool = False
    redeemed_by: str | None = None
    redeemed_at: datetime | None = None
