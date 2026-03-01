"""Build create certificate use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import CreateCertificateUseCase
from .build_certificate_repository_dependency import CertificateRepositoryDependency


def build_create_certificate_use_case(
    repository: CertificateRepositoryDependency,
) -> CreateCertificateUseCase:
    """Build a CreateCertificateUseCase with all dependencies injected.

    Intended to be used as a FastAPI Depends() provider. The repository
    is injected automatically via CertificateRepositoryDependency, which
    in turn receives its session from the PostgreSQL session dependency.

    Args:
        repository: Certificate repository injected by FastAPI.

    Returns:
        CreateCertificateUseCase: Use case instance ready for execution.
    """
    return CreateCertificateUseCase(repository=repository)


CreateCertificateUseCaseDependency = Annotated[
    CreateCertificateUseCase,
    Depends(build_create_certificate_use_case),
]
