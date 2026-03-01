"""Build get certificate use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GetCertificateUseCase
from .build_certificate_repository_dependency import CertificateRepositoryDependency


def build_get_certificate_use_case(
    repository: CertificateRepositoryDependency,
) -> GetCertificateUseCase:
    """Build a GetCertificateUseCase with all dependencies injected.

    Args:
        repository: Certificate repository injected by FastAPI.

    Returns:
        GetCertificateUseCase: Use case instance ready for execution.
    """
    return GetCertificateUseCase(repository=repository)


GetCertificateUseCaseDependency = Annotated[
    GetCertificateUseCase,
    Depends(build_get_certificate_use_case),
]
