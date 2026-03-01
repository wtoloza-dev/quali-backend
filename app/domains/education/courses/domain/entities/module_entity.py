"""Course module domain entity."""

from pydantic import BaseModel

from app.shared.entities import AuditEntity


class ModuleData(BaseModel):
    """Lean module data used by use cases that create a module.

    Attributes:
        course_id: The course this module belongs to.
        title: Human-readable title of the module.
        order: Position of this module within the course (1-based).
    """

    course_id: str
    title: str
    order: int


class ModuleEntity(ModuleData, AuditEntity):
    """Full module entity returned by the repository after persistence."""

    pass
