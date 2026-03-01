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
        company_id: ULID of the company (tenant scope).
        is_redeemed: Whether this code has been used.
        redeemed_by: ULID of the user who redeemed the code.
        redeemed_at: Timestamp when the code was redeemed.
    """

    __tablename__ = "access_codes"

    code: str = Field(nullable=False, unique=True, index=True)
    course_id: str = Field(nullable=False, index=True)
    company_id: str = Field(nullable=False)
    is_redeemed: bool = Field(default=False, nullable=False)
    redeemed_by: str | None = Field(default=None, nullable=True)
    redeemed_at: datetime | None = Field(
        default=None,
        nullable=True,
        sa_type=DateTime(timezone=True),
    )
