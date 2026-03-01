"""Training plans subdomain route handlers."""

from fastapi import APIRouter

from .add_training_plan_item_route import router as add_item_router
from .create_training_plan_route import router as create_router
from .delete_training_plan_route import router as delete_router
from .get_training_plan_route import router as get_router
from .list_training_plans_route import router as list_router
from .remove_training_plan_item_route import router as remove_item_router
from .update_training_plan_route import router as update_router


router = APIRouter()
router.include_router(list_router)
router.include_router(create_router)
router.include_router(get_router)
router.include_router(update_router)
router.include_router(delete_router)
router.include_router(add_item_router)
router.include_router(remove_item_router)

__all__ = ["router"]
