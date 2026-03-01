"""Education domain — aggregates subdomain routers."""

from fastapi import APIRouter

from app.domains.education.access_codes.presentation.routes import (
    router as access_codes_router,
)
from app.domains.education.courses.presentation.routes import router as courses_router


router = APIRouter()
router.include_router(courses_router)
router.include_router(access_codes_router)

__all__ = ["router"]
