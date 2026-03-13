"""Access codes subdomain route handlers."""

from fastapi import APIRouter

from .generate_access_codes_route import router as generate_access_codes_router
from .list_company_access_codes_route import router as list_company_access_codes_router
from .redeem_access_code_route import router as redeem_access_code_router


router = APIRouter()
router.include_router(generate_access_codes_router)
router.include_router(list_company_access_codes_router)
router.include_router(redeem_access_code_router)

__all__ = ["router"]
