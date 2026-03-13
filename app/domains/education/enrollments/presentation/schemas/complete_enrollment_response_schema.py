"""Complete enrollment response schema."""

from pydantic import BaseModel

from app.domains.certification.presentation.schemas import (
    CertificatePrivateResponseSchema,
)

from .enrollment_response_schema import EnrollmentResponseSchema


class CompleteEnrollmentResponseSchema(BaseModel):
    """Response returned when an enrollment is completed.

    Contains the updated enrollment and the newly issued certificate.

    Attributes:
        enrollment: The enrollment after being marked as completed.
        certificate: The certificate issued upon course completion.
    """

    enrollment: EnrollmentResponseSchema
    certificate: CertificatePrivateResponseSchema
