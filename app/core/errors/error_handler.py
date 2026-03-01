"""FastAPI exception handlers for domain and unexpected errors."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.shared.exceptions import DomainException

from .error_mapper import DomainExceptionMapper


logger = logging.getLogger(__name__)


async def domain_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle DomainException subclasses and convert them to HTTP responses.

    Args:
        request: The incoming HTTP request.
        exc: The raised DomainException instance.

    Returns:
        JSONResponse with the mapped status code and structured error body.
    """
    domain_exc = exc  # type: ignore[assignment]
    assert isinstance(domain_exc, DomainException)

    logger.warning(
        "Domain exception [%s] at %s %s: %s",
        domain_exc.error_code,
        request.method,
        request.url.path,
        domain_exc.message,
        extra={"context": domain_exc.context},
    )

    return JSONResponse(
        status_code=DomainExceptionMapper.get_status_code(domain_exc),
        content=DomainExceptionMapper.get_response_body(domain_exc),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions not covered by domain handlers.

    Args:
        request: The incoming HTTP request.
        exc: The unexpected exception.

    Returns:
        JSONResponse with a 500 status and a generic error body.
    """
    logger.error(
        "Unhandled exception [%s] at %s %s",
        type(exc).__name__,
        request.method,
        request.url.path,
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
            "context": {},
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    app.add_exception_handler(DomainException, domain_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, generic_exception_handler)
