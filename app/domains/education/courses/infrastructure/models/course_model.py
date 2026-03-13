"""Course SQLModel ORM model."""

import sqlalchemy as sa
from sqlmodel import Field

from app.shared.models import AuditModel

from ...domain.enums import CourseStatus, CourseVertical, CourseVisibility


class CourseModel(AuditModel, table=True):
    """SQLModel ORM representation of the courses table.

    Attributes:
        __tablename__: Database table name.
        company_id: Owning company (indexed). Quali is just another company.
        title: Human-readable course title.
        description: Optional longer description.
        vertical: Regulatory vertical (sst, food_quality, general).
        regulatory_ref: Optional regulatory clause reference.
        validity_days: Certificate validity period in days. None = no expiry.
        visibility: PUBLIC (all companies) or PRIVATE (owning company only).
        status: Lifecycle status (draft, published, archived).
    """

    __tablename__ = "courses"

    company_id: str = Field(nullable=False, index=True)
    title: str = Field(nullable=False)
    description: str | None = Field(default=None, nullable=True)
    vertical: CourseVertical = Field(sa_type=sa.String(), nullable=False)
    regulatory_ref: str | None = Field(default=None, nullable=True)
    validity_days: int | None = Field(default=None, nullable=True)
    visibility: CourseVisibility = Field(
        default=CourseVisibility.PRIVATE, sa_type=sa.String(), nullable=False
    )
    status: CourseStatus = Field(
        default=CourseStatus.DRAFT, sa_type=sa.String(), nullable=False
    )
