"""Create enrollments table.

Revision ID: 0006
Revises: 0005
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create enrollments table."""
    op.create_table(
        "enrollments",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("course_id", sa.String(), nullable=False),
        sa.Column("company_id", sa.String(), nullable=False),
        sa.Column("is_mandatory", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("status", sa.String(), server_default="not_started", nullable=False),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_enrollments_user_id", "enrollments", ["user_id"])
    op.create_index("ix_enrollments_course_id", "enrollments", ["course_id"])
    op.create_index("ix_enrollments_company_id", "enrollments", ["company_id"])


def downgrade() -> None:
    """Drop enrollments table."""
    op.drop_index("ix_enrollments_company_id", table_name="enrollments")
    op.drop_index("ix_enrollments_course_id", table_name="enrollments")
    op.drop_index("ix_enrollments_user_id", table_name="enrollments")
    op.drop_table("enrollments")
