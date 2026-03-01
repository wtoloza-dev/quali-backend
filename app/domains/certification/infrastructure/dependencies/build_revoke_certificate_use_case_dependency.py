"""Build revoke certificate use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import RevokeCertificateUseCase
from .build_certificate_repository_dependency import CertificateRepositoryDependency


def build_revoke_certificate_use_case(
    repository: CertificateRepositoryDependency,
) -> RevokeCertificateUseCase:
    """Build a RevokeCertificateUseCase with all dependencies injected.

    Args:
        repository: Certificate repository injected by FastAPI.

    Returns:
        RevokeCertificateUseCase: Use case instance ready for execution.
    """
    return RevokeCertificateUseCase(repository=repository)


RevokeCertificateUseCaseDependency = Annotated[
    RevokeCertificateUseCase,
    Depends(build_revoke_certificate_use_case),
]
