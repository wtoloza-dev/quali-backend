"""Enroll user use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.courses.infrastructure.dependencies import (
    CourseRepositoryDependency,
)

from ...application.use_cases import EnrollUserUseCase
from .build_enrollment_repository_dependency import EnrollmentRepositoryDependency


def build_enroll_user_use_case(
    repository: EnrollmentRepositoryDependency,
    course_repository: CourseRepositoryDependency,
) -> EnrollUserUseCase:
    """Build an EnrollUserUseCase with injected repositories.

    Args:
        repository: Enrollment repository injected by FastAPI.
        course_repository: Course repository injected by FastAPI.

    Returns:
        EnrollUserUseCase: Use case instance ready for execution.
    """
    return EnrollUserUseCase(
        repository=repository,
        course_repository=course_repository,
    )


EnrollUserUseCaseDependency = Annotated[
    EnrollUserUseCase,
    Depends(build_enroll_user_use_case),
]
