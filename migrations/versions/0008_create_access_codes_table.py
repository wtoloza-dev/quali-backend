"""Create access_codes table.

Revision ID: 0008
Revises: 0007
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008"
down_revision: str | None = "0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create access_codes table."""
    op.create_table(
        "access_codes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("course_id", sa.String(), nullable=False),
        sa.Column("company_id", sa.String(), nullable=False),
        sa.Column("is_redeemed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("redeemed_by", sa.String(), nullable=True),
        sa.Column("redeemed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_access_codes_code", "access_codes", ["code"], unique=True)
    op.create_index("ix_access_codes_course_id", "access_codes", ["course_id"])


def downgrade() -> None:
    """Drop access_codes table."""
    op.drop_index("ix_access_codes_course_id", table_name="access_codes")
    op.drop_index("ix_access_codes_code", table_name="access_codes")
    op.drop_table("access_codes")
