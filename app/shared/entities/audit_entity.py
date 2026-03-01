"""Shared audit entity base for all domain entities."""

from datetime import datetime

from pydantic import BaseModel


class AuditEntity(BaseModel):
    """Base entity carrying audit fields for all persisted domain objects.

    Domain entities that represent a row fetched from the database should
    inherit from this class to guarantee consistent audit field definitions
    across all domains.

    Mirrors AuditModel at the ORM layer — AuditModel owns the DB mapping,
    AuditEntity owns the domain representation.

    Attributes:
        id: ULID-based unique identifier, sortable by creation time.
        created_at: Timestamp when the record was created.
        created_by: ID of the user who created the record.
        updated_at: Timestamp of the last update, managed by the DB.
        updated_by: ID of the user who last updated the record.
    """

    id: str
    created_at: datetime
    created_by: str
    updated_at: datetime | None = None
    updated_by: str | None
