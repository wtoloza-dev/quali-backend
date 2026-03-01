"""Entity tombstone SQLModel ORM model."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel
from ulid import ULID


class EntityTombstoneModel(SQLModel, table=True):
    """Stores a JSON snapshot of any hard-deleted entity.

    When an entity is deleted, the repository saves its full state here
    before issuing a hard DELETE. This provides a deletions-only audit
    trail without polluting the main domain tables with soft-delete columns.

    Polymorphism is achieved via the entity_type discriminator column, so
    a single table handles deletions for all domains.

    Attributes:
        __tablename__: Database table name.
        id: ULID primary key for the tombstone record itself.
        entity_type: Domain name of the deleted entity (e.g. "user").
        entity_id: Original ULID of the deleted entity.
        payload: Full JSON snapshot of the entity state at deletion time.
        deleted_at: Timestamp when the deletion occurred.
        deleted_by: ULID of the actor who performed the deletion.
    """

    __tablename__ = "entity_tombstones"

    id: str = Field(
        default_factory=lambda: str(ULID()),
        primary_key=True,
        nullable=False,
    )
    entity_type: str = Field(nullable=False, index=True)
    entity_id: str = Field(nullable=False, index=True)
    payload: dict = Field(sa_type=sa.JSON, nullable=False)
    deleted_at: datetime = Field(
        nullable=False,
        sa_type=DateTime(timezone=True),
    )
    deleted_by: str = Field(nullable=False)
