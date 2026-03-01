"""Shared audit mixin for SQLModel ORM models."""

from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlmodel import Field, SQLModel
from ulid import ULID


class AuditModel(SQLModel):
    """Mixin that adds standard audit fields to any ORM model.

    All domain ORM models should inherit from this class to ensure
    consistent audit tracking across the system.

    ID strategy:
        Uses ULID (Universally Unique Lexicographically Sortable Identifier)
        instead of UUID. ULIDs are time-ordered, which means the primary key
        naturally reflects insertion order — no secondary sort column needed.

    Timestamp strategy:
        - created_at: set once on INSERT by the database.
        - updated_at: updated automatically on every UPDATE by the database.
          IMPORTANT: never set updated_at manually in Python. It must be
          managed by the DB engine (DEFAULT / ON UPDATE trigger or
          server_default) so it remains trustworthy regardless of which
          layer performs the update.

    Attributes:
        id: ULID-based primary key, sortable by creation time.
        created_at: Timestamp set by the DB when the row is inserted.
        created_by: ID of the user who created the record.
        updated_at: Timestamp updated by the DB on every row modification.
        updated_by: ID of the user who last updated the record.
    """

    id: str = Field(
        default_factory=lambda: str(ULID()),
        primary_key=True,
        nullable=False,
    )

    created_at: datetime = Field(
        default=None,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
    )

    created_by: str = Field(
        nullable=False,
    )

    # NOTE: updated_at must NOT be set in Python code. It is managed
    # entirely by the database via server_default + onupdate so that any
    # direct SQL update (migrations, admin tools) also keeps it accurate.
    updated_at: datetime = Field(
        default=None,
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": text("now()"),
        },
    )

    updated_by: str | None = Field(
        default=None,
        nullable=True,
    )
