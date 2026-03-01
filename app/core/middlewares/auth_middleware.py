"""Authentication middleware.

Pure ASGI middleware that extracts the Firebase ID token from the
Authorization header, verifies it, and stores the result in a
request-scoped ContextVar.

Intentionally soft — missing or invalid tokens do not produce a 401 here.
Routes that require authentication declare ``CurrentUserDependency`` or
``require_role()`` as a FastAPI dependency, which raises
UnauthorizedException if no context was set.
"""

import os

from starlette.types import ASGIApp, Receive, Scope, Send

from app.shared.auth.auth_context import AuthContext
from app.shared.auth.auth_context_var import reset_auth_context, set_auth_context
from app.shared.exceptions import UnauthorizedException
from app.shared.services.firebase_auth_service import get_firebase_auth_service


_SCOPE = os.getenv("SCOPE", "local")
_DEV_SEED_HEADER = "x-dev-seed"


class AuthMiddleware:
    """ASGI middleware that resolves the authenticated user per request.

    Reads the Authorization header, verifies the Bearer token via the
    Firebase Admin SDK, and writes the result into the request-scoped
    ContextVar. Downstream route handlers consume auth via
    ``CurrentUserDependency`` or ``require_role()``, not by calling
    ``get_auth_context()`` directly.

    Attributes:
        app: The next ASGI application in the middleware chain.
    """

    def __init__(self, app: ASGIApp) -> None:
        """Initialise the middleware with the next ASGI app in the chain.

        Args:
            app: The next ASGI application to call.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Process the request and populate the auth context if a valid token is present.

        Skips non-HTTP connections. On token decode failure, the context
        is left empty — the route decides whether authentication is required.

        Args:
            scope: ASGI connection scope.
            receive: ASGI receive channel.
            send: ASGI send channel.
        """
        reset_token = None
        if scope["type"] == "http":
            headers: dict[bytes, bytes] = dict(scope["headers"])
            raw_auth = headers.get(b"authorization", b"").decode()
            if raw_auth.startswith("Bearer "):
                bearer = raw_auth.removeprefix("Bearer ")
                try:
                    ctx = get_firebase_auth_service().decode(bearer)
                    reset_token = set_auth_context(ctx)
                except (UnauthorizedException, Exception):
                    pass  # soft fail — unauthenticated routes still work
            elif _SCOPE == "local" and headers.get(b"x-dev-seed"):
                # Local dev bypass: allow seed scripts to authenticate
                # by sending the x-dev-seed header with a fake user ID.
                fake_uid = headers[b"x-dev-seed"].decode()
                ctx = AuthContext(user_id=fake_uid, email="seed@localhost")
                reset_token = set_auth_context(ctx)

        try:
            await self.app(scope, receive, send)
        finally:
            if reset_token is not None:
                reset_auth_context(reset_token)
