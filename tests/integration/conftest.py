"""Shared fixtures for integration tests.

Reuses the session-scoped PostgreSQL container and async engine from
the root conftest. Provides a per-test async session and autouse
truncation for integration-specific tables.

Usage:
    uv run pytest -m integration
"""

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest_asyncio.fixture
async def session(async_engine) -> AsyncSession:
    """Per-test async session for direct repository testing."""
    factory = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with factory() as s:
        yield s


# Tables used by integration tests (subset — add as needed).
_TRUNCATE_TABLES = [
    "certificates",
    "company_members",
    "companies",
    "users",
]


@pytest_asyncio.fixture(autouse=True)
async def truncate_tables(async_engine):
    """Truncate domain tables before each integration test."""
    factory = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with factory() as s:
        for table in _TRUNCATE_TABLES:
            await s.exec(text(f"TRUNCATE TABLE {table} CASCADE"))
        await s.commit()
