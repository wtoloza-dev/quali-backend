"""PostgreSQL async session dependency.

Provides a per-request AsyncSession sourced from the connection pool
initialised during application startup (app.state.db).

Usage in a repository or route:
    from app.shared.dependencies.clients.sql import PostgresSessionDependency

    async def handle_create_certificate_route(
        session: PostgresSessionDependency,
        ...
    ) -> ...:
        ...
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_postgres_session_dependency(
    request: Request,
) -> AsyncGenerator[AsyncSession]:
    """Yield an async PostgreSQL session for the duration of a request.

    Borrows a connection from the pool stored in app.state.db (initialised
    by the lifespan). The connection is returned to the pool when the
    request completes, whether it succeeds or fails.

    Args:
        request: The incoming FastAPI request (injected automatically).

    Yields:
        AsyncSession: A SQLModel async session ready for database operations.
    """
    async with request.app.state.db.get_session() as session:
        yield session


PostgresSessionDependency = Annotated[
    AsyncSession, Depends(get_postgres_session_dependency)
]
