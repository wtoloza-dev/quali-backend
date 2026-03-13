"""Complete enrollment use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.certification.infrastructure.dependencies import (
    CertificateRepositoryDependency,
)
from app.domains.education.assessments.infrastructure.dependencies import (
    AttemptRepositoryDependency,
)
from app.domains.education.courses.infrastructure.dependencies import (
    CourseRepositoryDependency,
    ModuleRepositoryDependency,
)

from ...application.use_cases import CompleteEnrollmentUseCase
from .build_enrollment_repository_dependency import EnrollmentRepositoryDependency


def build_complete_enrollment_use_case(
    enrollment_repository: EnrollmentRepositoryDependency,
    attempt_repository: AttemptRepositoryDependency,
    course_repository: CourseRepositoryDependency,
    module_repository: ModuleRepositoryDependency,
    certificate_repository: CertificateRepositoryDependency,
) -> CompleteEnrollmentUseCase:
    """Build a CompleteEnrollmentUseCase with injected repositories.

    Args:
        enrollment_repository: Enrollment repository injected by FastAPI.
        attempt_repository: Attempt repository injected by FastAPI.
        course_repository: Course repository injected by FastAPI.
        module_repository: Module repository injected by FastAPI.
        certificate_repository: Certificate repository injected by FastAPI.

    Returns:
        CompleteEnrollmentUseCase: Use case instance ready for execution.
    """
    return CompleteEnrollmentUseCase(
        enrollment_repository=enrollment_repository,
        attempt_repository=attempt_repository,
        course_repository=course_repository,
        module_repository=module_repository,
        certificate_repository=certificate_repository,
    )


CompleteEnrollmentUseCaseDependency = Annotated[
    CompleteEnrollmentUseCase,
    Depends(build_complete_enrollment_use_case),
]
