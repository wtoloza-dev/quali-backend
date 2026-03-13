"""Enrollments subdomain route handlers."""

from fastapi import APIRouter

from .complete_enrollment_route import router as complete_enrollment_router
from .enroll_user_route import router as enroll_user_router
from .get_enrollment_route import router as get_enrollment_router
from .list_company_enrollments_route import router as list_company_enrollments_router
from .list_enrollments_route import router as list_enrollments_router
from .unenroll_route import router as unenroll_router
from .update_enrollment_status_route import router as update_enrollment_status_router


router = APIRouter()
router.include_router(list_company_enrollments_router)
router.include_router(list_enrollments_router)
router.include_router(enroll_user_router)
router.include_router(get_enrollment_router)
router.include_router(complete_enrollment_router)
router.include_router(update_enrollment_status_router)
router.include_router(unenroll_router)

__all__ = ["router"]
