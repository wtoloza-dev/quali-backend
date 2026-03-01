"""Legal acceptance ORM model."""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlmodel import Field, SQLModel
from ulid import ULID


class LegalAcceptanceModel(SQLModel, table=True):
    """Records a user's acceptance of a legal declaration at enrollment time.

    This is a write-only audit log. Once created, records are never
    updated or deleted.

    Attributes:
        id: ULID primary key.
        user_id: The user who accepted the declaration.
        enrollment_id: The enrollment this acceptance is tied to.
        acceptance_type: Category of declaration (e.g. "enrollment_identity").
        declaration_text: The exact legal text the user accepted.
        ip_address: Client IP at the time of acceptance.
        accepted_at: Timestamp when the user accepted.
    """

    __tablename__ = "legal_acceptances"

    id: str = Field(
        default_factory=lambda: str(ULID()),
        primary_key=True,
        nullable=False,
    )
    user_id: str = Field(nullable=False, index=True)
    enrollment_id: str = Field(nullable=False, index=True)
    acceptance_type: str = Field(nullable=False)
    declaration_text: str = Field(nullable=False)
    ip_address: str | None = Field(default=None, nullable=True)
    accepted_at: datetime = Field(
        default=None,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
    )
