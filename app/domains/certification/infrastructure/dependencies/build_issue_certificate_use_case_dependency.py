"""Build issue certificate use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import IssueCertificateUseCase
from .build_certificate_repository_dependency import CertificateRepositoryDependency


def build_issue_certificate_use_case(
    repository: CertificateRepositoryDependency,
) -> IssueCertificateUseCase:
    """Build an IssueCertificateUseCase with all dependencies injected.

    Args:
        repository: Certificate repository injected by FastAPI.

    Returns:
        IssueCertificateUseCase: Use case instance ready for execution.
    """
    return IssueCertificateUseCase(repository=repository)


IssueCertificateUseCaseDependency = Annotated[
    IssueCertificateUseCase,
    Depends(build_issue_certificate_use_case),
]
