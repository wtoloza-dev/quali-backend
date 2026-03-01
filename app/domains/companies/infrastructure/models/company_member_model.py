"""Company member SQLModel ORM model."""

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from app.shared.auth.role import Role
from app.shared.models import AuditModel


class CompanyMemberModel(AuditModel, table=True):
    """SQLModel ORM representation of the company_members table.

    Maps company membership data to the database. Used exclusively within
    the infrastructure layer — never returned directly to the application
    or presentation layers.

    No FK constraints are defined; referential integrity is enforced at the
    application level.

    Attributes:
        __tablename__: Database table name.
        company_id: ULID of the company; indexed for fast member lookups.
        user_id: ULID of the user; indexed for fast reverse lookups.
        role: Permission level within the company.
    """

    __tablename__ = "company_members"
    __table_args__ = (
        UniqueConstraint(
            "company_id", "user_id", name="uq_company_members_company_user"
        ),
    )

    company_id: str = Field(nullable=False, index=True)
    user_id: str = Field(nullable=False, index=True)
    role: Role = Field(sa_type=sa.String(), nullable=False)
