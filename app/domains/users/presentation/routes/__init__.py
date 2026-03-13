"""Users domain route handlers package."""

from fastapi import APIRouter

from .create_user_route import router as create_user_router
from .delete_user_route import router as delete_user_router
from .get_user_route import router as get_user_router
from .list_users_route import router as list_users_router
from .me_route import router as me_router
from .search_user_by_email_route import router as search_user_by_email_router
from .update_user_route import router as update_user_router


router = APIRouter()
router.include_router(me_router)
router.include_router(search_user_by_email_router)
router.include_router(list_users_router)
router.include_router(create_user_router)
router.include_router(get_user_router)
router.include_router(update_user_router)
router.include_router(delete_user_router)

__all__ = ["router"]
