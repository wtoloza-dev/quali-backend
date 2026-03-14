"""add slug to courses

Revision ID: 1c5b116ded15
Revises: b9c388c1420a
Create Date: 2026-03-12 22:24:43.026828

"""

import re
import unicodedata
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1c5b116ded15"
down_revision: str | Sequence[str] | None = "b9c388c1420a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text).strip("-")


def upgrade() -> None:
    """Upgrade schema."""
    # Add column as nullable first
    op.add_column("courses", sa.Column("slug", sa.String(), nullable=True))

    # Backfill existing rows with slugified title
    conn = op.get_bind()
    courses = conn.execute(sa.text("SELECT id, title FROM courses")).fetchall()
    for course in courses:
        slug = _slugify(course.title)
        conn.execute(
            sa.text("UPDATE courses SET slug = :slug WHERE id = :id"),
            {"slug": slug, "id": course.id},
        )

    # Make non-nullable and add unique index
    op.alter_column("courses", "slug", nullable=False)
    op.create_index(op.f("ix_courses_slug"), "courses", ["slug"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_courses_slug"), table_name="courses")
    op.drop_column("courses", "slug")
