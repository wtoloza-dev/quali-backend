"""Health check response schema."""

from pydantic import BaseModel


class HealthCheckResponseSchema(BaseModel):
    """Response schema for the health check endpoint.

    Attributes:
        status: Overall service status. 'ok' when all checks pass.
        database: Database connectivity status. 'ok' or 'unreachable'.
    """

    status: str
    database: str
