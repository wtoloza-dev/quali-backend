"""Course module SQLModel ORM model."""

from sqlmodel import Field

from app.shared.models import AuditModel


class ModuleModel(AuditModel, table=True):
    """SQLModel ORM representation of the course_modules table.

    Attributes:
        __tablename__: Database table name.
        course_id: Parent course (indexed).
        title: Human-readable module title.
        order: Position within the course (1-based, ascending).
    """

    __tablename__ = "course_modules"

    course_id: str = Field(nullable=False, index=True)
    title: str = Field(nullable=False)
    order: int = Field(nullable=False)
