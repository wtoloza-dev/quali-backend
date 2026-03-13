"""Redeem access code use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.enrollments.infrastructure.dependencies.build_enrollment_repository_dependency import (
    EnrollmentRepositoryDependency,
)

from ...application.use_cases import RedeemAccessCodeUseCase
from .build_access_code_repository_dependency import AccessCodeRepositoryDependency


def build_redeem_access_code_use_case(
    repository: AccessCodeRepositoryDependency,
    enrollment_repository: EnrollmentRepositoryDependency,
) -> RedeemAccessCodeUseCase:
    """Build a RedeemAccessCodeUseCase with all dependencies injected.

    Args:
        repository: Access code repository injected by FastAPI.
        enrollment_repository: Enrollment repository for access upgrades.

    Returns:
        RedeemAccessCodeUseCase: Use case instance ready for execution.
    """
    return RedeemAccessCodeUseCase(
        repository=repository,
        enrollment_repository=enrollment_repository,
    )


RedeemAccessCodeUseCaseDependency = Annotated[
    RedeemAccessCodeUseCase,
    Depends(build_redeem_access_code_use_case),
]
