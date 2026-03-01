"""Create legal_acceptances table.

Revision ID: 0010
Revises: 0009
Create Date: 2026-03-10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010"
down_revision: str | None = "0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create legal_acceptances table."""
    op.create_table(
        "legal_acceptances",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("enrollment_id", sa.String(), nullable=False),
        sa.Column("acceptance_type", sa.String(), nullable=False),
        sa.Column("declaration_text", sa.String(), nullable=False),
        sa.Column("ip_address", sa.String(), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_legal_acceptances_user_id", "legal_acceptances", ["user_id"])
    op.create_index("ix_legal_acceptances_enrollment_id", "legal_acceptances", ["enrollment_id"])


def downgrade() -> None:
    """Drop legal_acceptances table."""
    op.drop_index("ix_legal_acceptances_enrollment_id", table_name="legal_acceptances")
    op.drop_index("ix_legal_acceptances_user_id", table_name="legal_acceptances")
    op.drop_table("legal_acceptances")
