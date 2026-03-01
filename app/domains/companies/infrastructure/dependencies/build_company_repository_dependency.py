"""Company repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.company_repository import CompanyRepository


def build_company_repository(
    session: PostgresSessionDependency,
) -> CompanyRepository:
    """Build a CompanyRepository with an injected async session.

    Intended to be used as a FastAPI Depends() provider. The session is
    sourced from the shared PostgreSQL session dependency, which borrows
    a connection from the pool initialised at application startup.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        CompanyRepository: Repository instance ready for use.
    """
    return CompanyRepository(session=session)


CompanyRepositoryDependency = Annotated[
    CompanyRepository,
    Depends(build_company_repository),
]
