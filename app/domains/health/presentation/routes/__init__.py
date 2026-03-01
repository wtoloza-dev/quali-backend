"""Route handlers for the Health domain."""

from fastapi import APIRouter

from .health_check_route import router as health_check_router


router = APIRouter()
router.include_router(health_check_router)

__all__ = ["router"]
