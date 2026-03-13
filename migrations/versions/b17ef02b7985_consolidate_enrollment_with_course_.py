"""consolidate enrollment with course access

Revision ID: b17ef02b7985
Revises: 7b9fe59be1a4
Create Date: 2026-03-12 20:09:10.988643

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "b17ef02b7985"
down_revision: str | Sequence[str] | None = "7b9fe59be1a4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add new columns to enrollments (with server_default for existing rows).
    op.add_column(
        "enrollments",
        sa.Column(
            "access_type",
            sa.String(),
            nullable=False,
            server_default="preview",
        ),
    )
    op.add_column(
        "enrollments",
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "enrollments",
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
    )

    # 2. Migrate existing course_access data into enrollments.
    # Any enrollment that has a matching course_access record gets
    # upgraded to 'full' with the expiry date copied over.
    op.execute(
        """
        UPDATE enrollments e
        SET access_type = 'full',
            start_date  = ca.created_at,
            end_date    = ca.expires_at
        FROM course_access ca
        WHERE e.user_id   = ca.user_id
          AND e.course_id = ca.course_id
        """
    )

    # 3. Drop the course_access table (no longer needed).
    op.drop_index(op.f("ix_course_access_course_id"), table_name="course_access")
    op.drop_index(op.f("ix_course_access_user_id"), table_name="course_access")
    op.drop_table("course_access")

    # 4. Drop company_id from enrollments.
    op.drop_index(op.f("ix_enrollments_company_id"), table_name="enrollments")
    op.drop_column("enrollments", "company_id")

    # 5. Remove the server_default (only needed for backfill).
    op.alter_column("enrollments", "access_type", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "enrollments",
        sa.Column(
            "company_id", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    op.create_index(
        op.f("ix_enrollments_company_id"),
        "enrollments",
        ["company_id"],
        unique=False,
    )
    op.drop_column("enrollments", "end_date")
    op.drop_column("enrollments", "start_date")
    op.drop_column("enrollments", "access_type")
    op.create_table(
        "course_access",
        sa.Column(
            "id", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created_by",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_by",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "user_id", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "course_id", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "access_type", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "expires_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("course_access_pkey")),
    )
    op.create_index(
        op.f("ix_course_access_user_id"),
        "course_access",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_course_access_course_id"),
        "course_access",
        ["course_id"],
        unique=False,
    )
