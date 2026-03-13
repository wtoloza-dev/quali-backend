"""Access code ORM model."""

from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field

from app.shared.models.audit_model import AuditModel


class AccessCodeModel(AuditModel, table=True):
    """SQLModel ORM model for the access_codes table.

    Attributes:
        __tablename__: Database table name.
        code: Unique access code string (QUALI-XXXX-XXXX format).
        course_id: ULID of the course this code unlocks.
        is_redeemed: Whether this code has been used.
        redeemed_by: ULID of the user who redeemed the code.
        redeemed_at: Timestamp when the code was redeemed.
        enrollment_id: ULID of the enrollment upgraded on redemption.
    """

    __tablename__ = "access_codes"

    code: str = Field(nullable=False, unique=True, index=True)
    course_id: str = Field(nullable=False, index=True)
    is_redeemed: bool = Field(default=False, nullable=False)
    redeemed_by: str | None = Field(default=None, nullable=True)
    redeemed_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime(timezone=True),
    )
    enrollment_id: str | None = Field(default=None, nullable=True, index=True)
