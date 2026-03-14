"""Create shared tables (entity_tombstones).

Revision ID: 0001
Revises:
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create entity_tombstones table."""
    op.create_table(
        "entity_tombstones",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_by", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_entity_tombstones_entity_type", "entity_tombstones", ["entity_type"])
    op.create_index("ix_entity_tombstones_entity_id", "entity_tombstones", ["entity_id"])


def downgrade() -> None:
    """Drop entity_tombstones table."""
    op.drop_index("ix_entity_tombstones_entity_id", table_name="entity_tombstones")
    op.drop_index("ix_entity_tombstones_entity_type", table_name="entity_tombstones")
    op.drop_table("entity_tombstones")
