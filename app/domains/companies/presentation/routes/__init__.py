"""Companies domain route handlers package."""

from fastapi import APIRouter

from .add_company_member_route import router as add_company_member_router
from .create_company_route import router as create_company_router
from .delete_company_route import router as delete_company_router
from .get_company_member_me_route import router as get_company_member_me_router
from .get_company_members_route import router as get_company_members_router
from .get_company_route import router as get_company_router
from .list_companies_route import router as list_companies_router
from .remove_company_member_route import router as remove_company_member_router
from .update_company_member_route import router as update_company_member_router
from .update_company_route import router as update_company_router


router = APIRouter()
router.include_router(list_companies_router)
router.include_router(create_company_router)
router.include_router(get_company_router)
router.include_router(update_company_router)
router.include_router(delete_company_router)
router.include_router(add_company_member_router)
router.include_router(get_company_member_me_router)
router.include_router(get_company_members_router)
router.include_router(remove_company_member_router)
router.include_router(update_company_member_router)

__all__ = ["router"]
