"""Create companies and company_members tables.

Revision ID: 0003
Revises: 0002
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create companies and company_members tables."""
    op.create_table(
        "companies",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("company_type", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("legal_name", sa.String(), nullable=True),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("tax_type", sa.String(), nullable=True),
        sa.Column("tax_id", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_companies_slug", "companies", ["slug"], unique=True)

    op.create_table(
        "company_members",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("company_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("company_id", "user_id", name="uq_company_members_company_user"),
    )
    op.create_index("ix_company_members_company_id", "company_members", ["company_id"])
    op.create_index("ix_company_members_user_id", "company_members", ["user_id"])


def downgrade() -> None:
    """Drop companies and company_members tables."""
    op.drop_index("ix_company_members_user_id", table_name="company_members")
    op.drop_index("ix_company_members_company_id", table_name="company_members")
    op.drop_table("company_members")
    op.drop_index("ix_companies_slug", table_name="companies")
    op.drop_table("companies")
