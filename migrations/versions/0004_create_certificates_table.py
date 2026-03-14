"""Create certificates table.

Revision ID: 0004
Revises: 0003
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create certificates table."""
    op.create_table(
        "certificates",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=True),
        sa.Column("company_id", sa.String(), nullable=False),
        sa.Column("recipient_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_by", sa.String(), nullable=True),
        sa.Column("revoked_reason", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_certificates_company_id", "certificates", ["company_id"])
    op.create_index("ix_certificates_recipient_id", "certificates", ["recipient_id"])
    op.create_index("ix_certificates_token", "certificates", ["token"], unique=True)


def downgrade() -> None:
    """Drop certificates table."""
    op.drop_index("ix_certificates_token", table_name="certificates")
    op.drop_index("ix_certificates_recipient_id", table_name="certificates")
    op.drop_index("ix_certificates_company_id", table_name="certificates")
    op.drop_table("certificates")
