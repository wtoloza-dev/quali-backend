"""Build list certificates use case dependency."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import ListCertificatesUseCase
from .build_certificate_repository_dependency import CertificateRepositoryDependency


def build_list_certificates_use_case(
    repository: CertificateRepositoryDependency,
) -> ListCertificatesUseCase:
    """Build a ListCertificatesUseCase with all dependencies injected.

    Args:
        repository: Certificate repository injected by FastAPI.

    Returns:
        ListCertificatesUseCase: Use case instance ready for execution.
    """
    return ListCertificatesUseCase(repository=repository)


ListCertificatesUseCaseDependency = Annotated[
    ListCertificatesUseCase,
    Depends(build_list_certificates_use_case),
]
