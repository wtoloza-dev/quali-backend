"""Create assessment_questions and assessment_attempts tables.

Revision ID: 0007
Revises: 0006
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0007"
down_revision: str | None = "0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create assessments domain tables."""
    # ── assessment_questions ─────────────────────────────────
    op.create_table(
        "assessment_questions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("course_id", sa.String(), nullable=False),
        sa.Column("module_id", sa.String(), nullable=True),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("question_type", sa.String(), nullable=False),
        sa.Column("config", sa.JSON(), server_default="{}", nullable=False),
        sa.Column("randomize", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("order", sa.Integer(), server_default="0", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_assessment_questions_course_id", "assessment_questions", ["course_id"])
    op.create_index("ix_assessment_questions_module_id", "assessment_questions", ["module_id"])

    # ── assessment_attempts ──────────────────────────────────
    op.create_table(
        "assessment_attempts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("enrollment_id", sa.String(), nullable=False),
        sa.Column("module_id", sa.String(), nullable=True),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("answers", sa.JSON(), server_default="[]", nullable=False),
        sa.Column("correct_question_ids", sa.JSON(), server_default="[]", nullable=False),
        sa.Column("taken_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_assessment_attempts_enrollment_id", "assessment_attempts", ["enrollment_id"])
    op.create_index("ix_assessment_attempts_module_id", "assessment_attempts", ["module_id"])


def downgrade() -> None:
    """Drop assessments domain tables."""
    op.drop_index("ix_assessment_attempts_module_id", table_name="assessment_attempts")
    op.drop_index("ix_assessment_attempts_enrollment_id", table_name="assessment_attempts")
    op.drop_table("assessment_attempts")
    op.drop_index("ix_assessment_questions_module_id", table_name="assessment_questions")
    op.drop_index("ix_assessment_questions_course_id", table_name="assessment_questions")
    op.drop_table("assessment_questions")
