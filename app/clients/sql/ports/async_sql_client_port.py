"""Async SQL client port.

Defines the structural interface all async database adapters must satisfy.
HTTP and framework concerns are excluded — this is pure infrastructure contract.
"""

from collections.abc import AsyncGenerator
from typing import Protocol

from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncSQLClientPort(Protocol):
    """Port (interface) for asynchronous SQL database clients.

    Any async database adapter (PostgreSQL, etc.) must structurally
    satisfy this protocol. Engine lifecycle is managed externally via
    FastAPI lifespan events — adapters are created once on startup
    and sessions are yielded per request.

    Example:
        >>> async with client.get_session() as session:
        ...     result = await session.exec(select(CertificateModel))
        ...     certificates = result.all()
    """

    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        """Yield an async database session for a single unit of work.

        Yields:
            AsyncSession: SQLModel async session scoped to a single request.
        """
        ...
