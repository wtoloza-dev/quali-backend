"""User repository dependency factory."""

from typing import Annotated

from fastapi import Depends

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..repositories.user_repository import UserRepository


def build_user_repository(
    session: PostgresSessionDependency,
) -> UserRepository:
    """Build a UserRepository with an injected async session.

    Intended to be used as a FastAPI Depends() provider. The session is
    sourced from the shared PostgreSQL session dependency, which borrows
    a connection from the pool initialised at application startup.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        UserRepository: Repository instance ready for use.
    """
    return UserRepository(session=session)


UserRepositoryDependency = Annotated[
    UserRepository,
    Depends(build_user_repository),
]
