"""Access code repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.access_code_repository import AccessCodeRepository


def build_access_code_repository(
    session: PostgresSessionDependency,
) -> AccessCodeRepository:
    """Build an AccessCodeRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        AccessCodeRepository: Repository instance ready for use.
    """
    return AccessCodeRepository(session=session)


AccessCodeRepositoryDependency = Annotated[
    AccessCodeRepository,
    Depends(build_access_code_repository),
]
