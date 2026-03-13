"""Courses subdomain route handlers."""

from fastapi import APIRouter

from .archive_course_route import router as archive_course_router
from .check_course_access_route import router as check_course_access_router
from .create_course_route import router as create_course_router
from .create_lesson_route import router as create_lesson_router
from .create_module_route import router as create_module_router
from .delete_course_route import router as delete_course_router
from .delete_lesson_route import router as delete_lesson_router
from .delete_module_route import router as delete_module_router
from .get_course_route import router as get_course_router
from .get_lesson_route import router as get_lesson_router
from .list_courses_route import router as list_courses_router
from .list_lessons_route import router as list_lessons_router
from .list_modules_route import router as list_modules_router
from .publish_course_route import router as publish_course_router
from .reorder_lessons_route import router as reorder_lessons_router
from .reorder_modules_route import router as reorder_modules_router
from .update_course_route import router as update_course_router
from .update_lesson_route import router as update_lesson_router
from .update_module_route import router as update_module_router


router = APIRouter()
router.include_router(list_courses_router)
router.include_router(create_course_router)
router.include_router(get_course_router)
router.include_router(check_course_access_router)
router.include_router(update_course_router)
router.include_router(publish_course_router)
router.include_router(archive_course_router)
router.include_router(delete_course_router)
router.include_router(list_modules_router)
router.include_router(create_module_router)
router.include_router(update_module_router)
router.include_router(reorder_modules_router)
router.include_router(delete_module_router)
router.include_router(create_lesson_router)
router.include_router(update_lesson_router)
router.include_router(list_lessons_router)
router.include_router(get_lesson_router)
router.include_router(reorder_lessons_router)
router.include_router(delete_lesson_router)

__all__ = ["router"]
