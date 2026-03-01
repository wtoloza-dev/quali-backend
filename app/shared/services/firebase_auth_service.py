"""Firebase token verification service.

Verifies Firebase ID tokens using Google's public keys directly,
without requiring a service account or Application Default Credentials.
"""

import os
from functools import lru_cache

import jwt
from jwt import PyJWKClient

from app.shared.auth.auth_context import AuthContext
from app.shared.exceptions import UnauthorizedException


GOOGLE_CERTS_URL = "https://www.googleapis.com/robot/v1/metadata/jwk/securetoken@system.gserviceaccount.com"
ISSUER_PREFIX = "https://securetoken.google.com/"


class FirebaseAuthService:
    """Verifies Firebase ID tokens using Google's public JWKs.

    No service account or ADC required — only FIREBASE_PROJECT_ID.
    """

    def __init__(self, project_id: str) -> None:
        self._project_id = project_id
        self._issuer = f"{ISSUER_PREFIX}{project_id}"
        self._jwk_client = PyJWKClient(GOOGLE_CERTS_URL, cache_keys=True)

    def decode(self, token: str) -> AuthContext:
        """Verify a Firebase ID token and return the authenticated context."""
        try:
            signing_key = self._jwk_client.get_signing_key_from_jwt(token)
            decoded = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self._project_id,
                issuer=self._issuer,
            )
            # Firebase tokens must have a subject (uid)
            uid = decoded.get("sub") or decoded.get("user_id")
            if not uid:
                raise UnauthorizedException(
                    message="Invalid access token.",
                    error_code="INVALID_TOKEN",
                )
            return AuthContext(
                user_id=uid,
                email=decoded.get("email", ""),
            )
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException(
                message="Access token has expired.",
                error_code="TOKEN_EXPIRED",
            )
        except (jwt.InvalidTokenError, Exception):
            raise UnauthorizedException(
                message="Invalid access token.",
                error_code="INVALID_TOKEN",
            )


@lru_cache
def get_firebase_auth_service() -> FirebaseAuthService:
    """Return the shared FirebaseAuthService singleton."""
    project_id = os.getenv("FIREBASE_PROJECT_ID", "")
    if not project_id:
        raise RuntimeError("FIREBASE_PROJECT_ID environment variable is required")
    return FirebaseAuthService(project_id)
