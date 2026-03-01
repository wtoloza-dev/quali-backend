"""Attempt repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.attempt_repository import AttemptRepository


def build_attempt_repository(
    session: PostgresSessionDependency,
) -> AttemptRepository:
    """Build an AttemptRepository with an injected async session.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        AttemptRepository: Repository instance ready for use.
    """
    return AttemptRepository(session=session)


AttemptRepositoryDependency = Annotated[
    AttemptRepository,
    Depends(build_attempt_repository),
]
