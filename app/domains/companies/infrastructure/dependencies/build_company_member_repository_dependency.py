"""Company member repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.company_member_repository import CompanyMemberRepository


def build_company_member_repository(
    session: PostgresSessionDependency,
) -> CompanyMemberRepository:
    """Build a CompanyMemberRepository with an injected async session.

    Intended to be used as a FastAPI Depends() provider. The session is
    sourced from the shared PostgreSQL session dependency, which borrows
    a connection from the pool initialised at application startup.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        CompanyMemberRepository: Repository instance ready for use.
    """
    return CompanyMemberRepository(session=session)


CompanyMemberRepositoryDependency = Annotated[
    CompanyMemberRepository,
    Depends(build_company_member_repository),
]
