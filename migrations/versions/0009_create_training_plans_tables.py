"""Create training_plans and training_plan_items tables.

Revision ID: 0009
Revises: 0008
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0009"
down_revision: str | None = "0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create training plans domain tables."""
    # ── training_plans ───────────────────────────────────────
    op.create_table(
        "training_plans",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("company_id", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("status", sa.String(), server_default="draft", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_training_plans_company_id", "training_plans", ["company_id"])

    # ── training_plan_items ──────────────────────────────────
    op.create_table(
        "training_plan_items",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("plan_id", sa.String(), nullable=False),
        sa.Column("course_id", sa.String(), nullable=False),
        sa.Column("target_role", sa.String(), nullable=True),
        sa.Column("scheduled_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_training_plan_items_plan_id", "training_plan_items", ["plan_id"])
    op.create_index("ix_training_plan_items_course_id", "training_plan_items", ["course_id"])


def downgrade() -> None:
    """Drop training plans domain tables."""
    op.drop_index("ix_training_plan_items_course_id", table_name="training_plan_items")
    op.drop_index("ix_training_plan_items_plan_id", table_name="training_plan_items")
    op.drop_table("training_plan_items")
    op.drop_index("ix_training_plans_company_id", table_name="training_plans")
    op.drop_table("training_plans")
