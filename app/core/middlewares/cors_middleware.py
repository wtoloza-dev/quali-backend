"""CORS middleware configuration.

Configures Cross-Origin Resource Sharing for the Quali API, allowing
requests from the known frontend origins (training, company, and admin apps).
"""

from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp


ALLOWED_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "https://quali.tchunza.com",
    "https://admin.quali.tchunza.com",
]

ALLOWED_ORIGIN_REGEX: str = r"https://\w+\.quali\.tchunza\.com"


class QualiCORSMiddleware(CORSMiddleware):
    """CORS middleware pre-configured with Quali's allowed origins.

    Wraps Starlette's CORSMiddleware with the fixed set of frontend
    origins plus a regex for company subdomains (``*.quali.tchunza.com``)
    so that ``main.py`` can register it with a plain
    ``app.add_middleware(QualiCORSMiddleware)`` call.
    """

    def __init__(self, app: ASGIApp) -> None:
        """Initialise the CORS middleware with Quali's allowed origins.

        Args:
            app: The next ASGI application in the middleware chain.
        """
        super().__init__(
            app,
            allow_origins=ALLOWED_ORIGINS,
            allow_origin_regex=ALLOWED_ORIGIN_REGEX,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
