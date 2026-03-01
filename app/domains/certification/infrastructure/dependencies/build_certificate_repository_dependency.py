"""Certificate repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.certificate_repository import CertificateRepository


def build_certificate_repository(
    session: PostgresSessionDependency,
) -> CertificateRepository:
    """Build a CertificateRepository with an injected async session.

    Intended to be used as a FastAPI Depends() provider. The session is
    sourced from the shared PostgreSQL session dependency, which borrows
    a connection from the pool initialised at application startup.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        CertificateRepository: Repository instance ready for use.
    """
    return CertificateRepository(session=session)


CertificateRepositoryDependency = Annotated[
    CertificateRepository,
    Depends(build_certificate_repository),
]
