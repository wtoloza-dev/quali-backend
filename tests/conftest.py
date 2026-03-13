"""Global test configuration.

Sets SCOPE=test before any app module is imported. Provides shared
database infrastructure (testcontainers PostgreSQL) and a ``client``
fixture for e2e tests backed by a real database session.

Unit tests are unaffected — the DB fixtures are lazy and only start
when a test requests ``client`` or ``async_engine``.
"""

import os
import subprocess
from pathlib import Path


os.environ.setdefault("SCOPE", "test")

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlmodel.ext.asyncio.session import AsyncSession
from testcontainers.postgres import PostgresContainer


# ---------------------------------------------------------------------------
# Colima (macOS) Docker socket detection
# ---------------------------------------------------------------------------
_COLIMA_SOCKET = Path.home() / ".colima" / "default" / "docker.sock"
if _COLIMA_SOCKET.exists() and not os.environ.get("DOCKER_HOST"):
    os.environ["DOCKER_HOST"] = f"unix://{_COLIMA_SOCKET}"
    os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")

_PG_IMAGE = "postgres:16-alpine"
_PG_USER = "test"
_PG_PASSWORD = "test"
_PG_DB = "test"


# ---------------------------------------------------------------------------
# Session-scoped database infrastructure (shared by e2e + integration tests)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def pg_container():
    """Start a PostgreSQL container for the entire test session."""
    with PostgresContainer(
        image=_PG_IMAGE,
        username=_PG_USER,
        password=_PG_PASSWORD,
        dbname=_PG_DB,
    ) as container:
        yield container


@pytest.fixture(scope="session")
def pg_sync_url(pg_container):
    """Plain postgresql:// URL used by Alembic and sync truncation."""
    return pg_container.get_connection_url().replace("+psycopg2", "")


@pytest.fixture(scope="session")
def pg_async_url(pg_container):
    """Asyncpg URL used by the SQLAlchemy async engine."""
    return pg_container.get_connection_url().replace("+psycopg2", "+asyncpg")


@pytest.fixture(scope="session")
def _run_migrations(pg_sync_url):
    """Run Alembic migrations once per session."""
    result = subprocess.run(
        ["uv", "run", "alembic", "upgrade", "head"],
        env={**os.environ, "DATABASE_URL": pg_sync_url},
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Alembic migration failed:\n{result.stderr}")


@pytest.fixture(scope="session")
def async_engine(pg_async_url, _run_migrations):
    """Shared async engine for the entire test session."""
    engine = create_async_engine(pg_async_url, echo=False, poolclass=NullPool)
    yield engine


@pytest.fixture(scope="session")
def sync_engine(pg_sync_url, _run_migrations):
    """Shared sync engine for truncation between e2e tests."""
    engine = create_engine(pg_sync_url, echo=False)
    yield engine
    engine.dispose()


# ---------------------------------------------------------------------------
# All domain tables (CASCADE makes order irrelevant)
# ---------------------------------------------------------------------------
_ALL_TABLES = [
    "entity_tombstones",
    "legal_acceptances",
    "assessment_attempts",
    "assessment_questions",
    "access_codes",
    "course_lessons",
    "course_modules",
    "enrollments",
    "courses",
    "training_plan_items",
    "training_plans",
    "certificates",
    "company_members",
    "companies",
    "users",
]


# ---------------------------------------------------------------------------
# E2e client fixture — real DB, only 2 overrides
# ---------------------------------------------------------------------------
TEST_USER_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAU"
TEST_EMAIL = "test@example.com"


@pytest.fixture
def client(async_engine, sync_engine):
    """TestClient backed by a real test database.

    Truncates all tables before each test for isolation. Overrides only
    ``get_postgres_session_dependency`` (session) and ``get_current_user``
    (auth). All repositories and contract adapters resolve naturally
    through the DI chain.
    """
    from fastapi.testclient import TestClient

    from app.main import app
    from app.shared.auth.auth_context import AuthContext
    from app.shared.auth.dependencies import get_current_user
    from app.shared.dependencies.clients.sql.postgres_session_dependency import (
        get_postgres_session_dependency,
    )

    # 1. Truncate all tables (sync — simple and fast)
    with sync_engine.begin() as conn:
        for table in _ALL_TABLES:
            conn.execute(text(f"TRUNCATE TABLE {table} CASCADE"))

    # 2. Override session dependency → test DB
    _factory = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False,
    )

    async def _test_session():
        async with _factory() as session:
            async with session.begin():
                yield session

    # 3. Override auth → fake user
    _fake_auth = AuthContext(user_id=TEST_USER_ID, email=TEST_EMAIL)

    app.dependency_overrides[get_postgres_session_dependency] = _test_session
    app.dependency_overrides[get_current_user] = lambda: _fake_auth

    yield TestClient(app)

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Seed fixtures — create prerequisite data via the API
# ---------------------------------------------------------------------------
@pytest.fixture
def company(client):
    """Create a company (auto-grants OWNER to test user)."""
    response = client.post(
        "/api/v1/companies/",
        json={
            "name": "Test Company",
            "slug": "test-company",
            "company_type": "organization",
            "email": "test@company.com",
            "country": "CO",
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def course(client, company):
    """Create a course under the test company."""
    response = client.post(
        f"/api/v1/companies/{company['id']}/education/courses/",
        json={"title": "Test Course", "vertical": "general"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def enrollment(client, company, course):
    """Enroll the test user in the test course."""
    response = client.post(
        f"/api/v1/companies/{company['id']}/education/enrollments/",
        json={"course_id": course["id"], "legal_accepted": True},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def user(client):
    """Create the test user profile via POST /me."""
    response = client.post("/api/v1/users/me")
    assert response.status_code == 201
    return response.json()
