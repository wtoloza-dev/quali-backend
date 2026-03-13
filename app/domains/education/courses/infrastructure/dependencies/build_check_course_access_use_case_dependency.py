"""Build check course access use case dependency."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.enrollments.infrastructure.dependencies.build_enrollment_repository_dependency import (
    EnrollmentRepositoryDependency,
)

from ...application.use_cases import CheckCourseAccessUseCase


def build_check_course_access_use_case(
    enrollment_repository: EnrollmentRepositoryDependency,
) -> CheckCourseAccessUseCase:
    """Build a CheckCourseAccessUseCase with all dependencies injected.

    Args:
        enrollment_repository: Enrollment repository injected by FastAPI.

    Returns:
        CheckCourseAccessUseCase: Use case instance ready for execution.
    """
    return CheckCourseAccessUseCase(
        enrollment_repository=enrollment_repository,
    )


CheckCourseAccessUseCaseDependency = Annotated[
    CheckCourseAccessUseCase,
    Depends(build_check_course_access_use_case),
]
