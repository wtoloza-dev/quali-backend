"""Health check route handler."""

import logging

from fastapi import APIRouter
from sqlalchemy import text

from app.shared.dependencies.clients.sql import PostgresSessionDependency

from ..schemas import HealthCheckResponseSchema


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    path="/",
    summary="Health check",
    description="Returns the status of the service and its infrastructure dependencies.",
)
async def handle_health_check_route(
    session: PostgresSessionDependency,
) -> HealthCheckResponseSchema:
    """Handle GET requests to verify service and database health.

    Executes a lightweight SELECT 1 against the database to confirm
    the connection pool is operational.

    Args:
        session: Async database session injected by FastAPI.

    Returns:
        HealthCheckResponseSchema: Status of the service and database.
    """
    try:
        await session.exec(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        logger.exception("Database health check failed.")
        db_status = "unreachable"

    return HealthCheckResponseSchema(
        status="ok" if db_status == "ok" else "degraded",
        database=db_status,
    )
