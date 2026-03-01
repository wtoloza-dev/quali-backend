"""Application lifespan — startup and shutdown event management."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.sql.adapters import AsyncPostgresAdapter
from app.core.settings import settings


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Manage application startup and shutdown events.

    Startup:
        - Initialise the async PostgreSQL connection pool.
        - Store the adapter in app.state for use across the application.

    Shutdown:
        - Dispose the connection pool and close all active connections.

    Args:
        app: The FastAPI application instance.

    Yields:
        None: Control passes to the running application.
    """
    logger.info("Starting up — initialising database connection pool.")

    app.state.db = AsyncPostgresAdapter(
        database_url=settings.DATABASE_URL,
        echo=settings.DEBUG,
    )

    yield

    logger.info("Shutting down — disposing database connection pool.")
    await app.state.db.engine.dispose()
