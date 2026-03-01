"""Certification domain route handlers package.

Exports two routers with different mounting strategies:

- ``company_router``: Company-scoped protected routes (issue, list, get, revoke).
  Mount under ``/companies/{company_id}/certificates`` so that ``require_role``
  can read the company ULID from the URL path.

- ``verify_router``: Public token-verification route.
  Mount under ``/certificates`` — no company context required to scan a QR code.
"""

from fastapi import APIRouter

from .get_certificate_route import router as get_certificate_router
from .issue_certificate_route import router as issue_certificate_router
from .list_certificates_route import router as list_certificates_router
from .revoke_certificate_route import router as revoke_certificate_router
from .verify_certificate_route import router as verify_certificate_router


company_router = APIRouter()

# NOTE: revoke (/{id}/revoke) MUST be included before get (/{id}) so FastAPI
# does not capture the literal "revoke" path segment as a certificate_id.
company_router.include_router(issue_certificate_router)
company_router.include_router(list_certificates_router)
company_router.include_router(revoke_certificate_router)
company_router.include_router(get_certificate_router)

verify_router = APIRouter()
verify_router.include_router(verify_certificate_router)

__all__ = [
    "company_router",
    "verify_router",
]
