"""Observability middleware.

Pure ASGI middleware that logs the HTTP method, path, response status,
and elapsed time for every incoming request. Avoids BaseHTTPMiddleware
limitations with contextvars propagation.
"""

import logging
import time

from starlette.types import ASGIApp, Receive, Scope, Send


logger = logging.getLogger(__name__)


class ObservabilityMiddleware:
    """ASGI middleware for minimum-standard request observability.

    Captures and logs the following per request:
        - HTTP method
        - Request path
        - Response status code
        - Elapsed time in milliseconds

    Example log output:
        GET /api/v1/certification/ 201 12.43ms
    """

    def __init__(self, app: ASGIApp) -> None:
        """Initialise the middleware with the next ASGI app in the chain.

        Args:
            app: The next ASGI application to call.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Process the request and log observability data.

        Skips non-HTTP connections (e.g. WebSocket, lifespan events).

        Args:
            scope: ASGI connection scope.
            receive: ASGI receive channel.
            send: ASGI send channel.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method: str = scope["method"]
        path: str = scope["path"]
        status_code: int = 0
        started_at: float = time.perf_counter()

        async def send_wrapper(message: dict) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        await self.app(scope, receive, send_wrapper)

        elapsed_ms: float = (time.perf_counter() - started_at) * 1000

        logger.info(
            "%s %s %s %.2fms",
            method,
            path,
            status_code,
            elapsed_ms,
        )
