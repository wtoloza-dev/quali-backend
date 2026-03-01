"""Redeem access code use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.domains.education.courses.infrastructure.dependencies import (
    GrantCourseAccessUseCaseDependency,
)

from ...application.use_cases import RedeemAccessCodeUseCase
from .build_access_code_repository_dependency import AccessCodeRepositoryDependency


def build_redeem_access_code_use_case(
    repository: AccessCodeRepositoryDependency,
    grant_access_use_case: GrantCourseAccessUseCaseDependency,
) -> RedeemAccessCodeUseCase:
    """Build a RedeemAccessCodeUseCase with all dependencies injected.

    Args:
        repository: Access code repository injected by FastAPI.
        grant_access_use_case: Use case to grant course access upon redemption.

    Returns:
        RedeemAccessCodeUseCase: Use case instance ready for execution.
    """
    return RedeemAccessCodeUseCase(
        repository=repository,
        grant_access_use_case=grant_access_use_case,
    )


RedeemAccessCodeUseCaseDependency = Annotated[
    RedeemAccessCodeUseCase,
    Depends(build_redeem_access_code_use_case),
]
