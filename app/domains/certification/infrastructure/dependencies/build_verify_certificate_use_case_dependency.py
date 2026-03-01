"""Build verify certificate use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import VerifyCertificateUseCase
from .build_certificate_repository_dependency import CertificateRepositoryDependency


def build_verify_certificate_use_case(
    repository: CertificateRepositoryDependency,
) -> VerifyCertificateUseCase:
    """Build a VerifyCertificateUseCase with all dependencies injected.

    Args:
        repository: Certificate repository injected by FastAPI.

    Returns:
        VerifyCertificateUseCase: Use case instance ready for execution.
    """
    return VerifyCertificateUseCase(repository=repository)


VerifyCertificateUseCaseDependency = Annotated[
    VerifyCertificateUseCase,
    Depends(build_verify_certificate_use_case),
]
