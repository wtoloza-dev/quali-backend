"""Update enrollment status request schema."""

from pydantic import BaseModel

from ...domain.enums import EnrollmentStatus


class UpdateEnrollmentStatusRequestSchema(BaseModel):
    """Request body for updating an enrollment's status.

    Attributes:
        status: The new enrollment lifecycle state.
    """

    status: EnrollmentStatus
