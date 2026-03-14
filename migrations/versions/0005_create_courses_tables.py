"""Create courses, course_modules, course_lessons, and course_access tables.

Revision ID: 0005
Revises: 0004
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create courses domain tables."""
    # ── courses ──────────────────────────────────────────────
    op.create_table(
        "courses",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("company_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("vertical", sa.String(), nullable=False),
        sa.Column("regulatory_ref", sa.String(), nullable=True),
        sa.Column("validity_days", sa.Integer(), nullable=True),
        sa.Column("passing_score", sa.Integer(), server_default="80", nullable=False),
        sa.Column("max_attempts", sa.Integer(), server_default="3", nullable=False),
        sa.Column("is_mandatory", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("visibility", sa.String(), server_default="private", nullable=False),
        sa.Column("status", sa.String(), server_default="draft", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_courses_company_id", "courses", ["company_id"])

    # ── course_modules ───────────────────────────────────────
    op.create_table(
        "course_modules",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("course_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_course_modules_course_id", "course_modules", ["course_id"])

    # ── course_lessons ───────────────────────────────────────
    op.create_table(
        "course_lessons",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("module_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.JSON(), server_default="[]", nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("is_preview", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_course_lessons_module_id", "course_lessons", ["module_id"])

    # ── course_access ────────────────────────────────────────
    op.create_table(
        "course_access",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("course_id", sa.String(), nullable=False),
        sa.Column("access_type", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_course_access_user_id", "course_access", ["user_id"])
    op.create_index("ix_course_access_course_id", "course_access", ["course_id"])


def downgrade() -> None:
    """Drop courses domain tables."""
    op.drop_index("ix_course_access_course_id", table_name="course_access")
    op.drop_index("ix_course_access_user_id", table_name="course_access")
    op.drop_table("course_access")
    op.drop_index("ix_course_lessons_module_id", table_name="course_lessons")
    op.drop_table("course_lessons")
    op.drop_index("ix_course_modules_course_id", table_name="course_modules")
    op.drop_table("course_modules")
    op.drop_index("ix_courses_company_id", table_name="courses")
    op.drop_table("courses")
