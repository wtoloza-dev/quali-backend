"""Async PostgreSQL adapter."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncPostgresAdapter:
    """Async PostgreSQL database adapter using SQLAlchemy + SQLModel.

    Manages an async connection pool and yields per-request sessions.
    Must be initialised once on application startup (via lifespan) and
    disposed on shutdown.

    Attributes:
        engine: The underlying SQLAlchemy async engine.

    Example:
        >>> adapter = AsyncPostgresAdapter(
        ...     database_url="postgresql+asyncpg://user:pass@localhost:5432/db",
        ...     echo=True,
        ... )
        >>> async with adapter.get_session() as session:
        ...     result = await session.exec(select(CertificateModel))
    """

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_recycle: int = 3600,
        pool_pre_ping: bool = True,
    ) -> None:
        """Initialise the adapter and create the async connection pool.

        Args:
            database_url: PostgreSQL DSN with asyncpg driver.
                Format: postgresql+asyncpg://user:pass@host:port/db
            echo: Log all SQL statements. Useful for debugging.
            pool_size: Permanent connections kept in the pool.
            max_overflow: Extra connections allowed beyond pool_size.
            pool_recycle: Seconds before a connection is recycled.
            pool_pre_ping: Test connections before use to detect stale ones.
        """
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
            pool_pre_ping=pool_pre_ping,
        )
        self._session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        """Yield an async session scoped to a single unit of work.

        Wraps the session in a transaction via ``session.begin()``.
        The transaction commits automatically when the request completes
        without error, and rolls back automatically on any exception.
        Repositories must call ``flush()`` instead of ``commit()`` so
        all operations within a request share the same transaction.

        Yields:
            AsyncSession: SQLModel async session bound to an open transaction.
        """
        async with self._session_factory() as session:
            async with session.begin():
                yield session
