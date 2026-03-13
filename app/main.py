"""Quali API application factory.

Registers all domain routers and configures the FastAPI application
instance used as the entry point for the entire backend.
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.errors import register_error_handlers
from app.core.lifespans import lifespan
from app.core.middlewares import AuthMiddleware, ObservabilityMiddleware
from app.core.settings import settings
from app.domains.certification.presentation.routes import (
    company_router as cert_company_router,
)
from app.domains.certification.presentation.routes import (
    verify_router as cert_verify_router,
)
from app.domains.companies.presentation.routes import router as companies_router
from app.domains.compliance.presentation.routes import router as compliance_router
from app.domains.education import router as education_router
from app.domains.education.access_codes.presentation.routes import (
    router as access_codes_router,
)
from app.domains.education.assessments.presentation.routes import (
    attempts_router as assessment_attempts_router,
)
from app.domains.education.assessments.presentation.routes import (
    questions_router as assessment_questions_router,
)
from app.domains.education.courses.presentation.routes.global_courses_route import (
    router as global_courses_router,
)
from app.domains.education.enrollments.presentation.routes import (
    router as enrollments_router,
)
from app.domains.education.training_plans.presentation.routes import (
    router as training_plans_router,
)
from app.domains.health.presentation.routes import router as health_router
from app.domains.quality_ops.presentation.routes import router as quality_ops_router
from app.domains.users.presentation.routes import router as users_router


def register_routes(app: FastAPI) -> None:
    """Register all domain routes under the /api/v1 prefix.

    Args:
        app: The FastAPI application instance to register the routes to.
    """
    api_v1_router = APIRouter(prefix="/api/v1")
    api_v1_router.include_router(
        companies_router, prefix="/companies", tags=["Companies"]
    )
    api_v1_router.include_router(users_router, prefix="/users", tags=["Users"])
    api_v1_router.include_router(
        cert_company_router,
        prefix="/companies/{company_id}/certificates",
        tags=["Certification"],
    )
    api_v1_router.include_router(
        cert_verify_router,
        prefix="/certificates",
        tags=["Certification"],
    )
    # Education — Courses
    api_v1_router.include_router(
        education_router,
        prefix="/companies/{company_id}/education/courses",
        tags=["Education — Courses"],
    )
    # Education — All Courses (superadmin, global)
    api_v1_router.include_router(
        global_courses_router,
        prefix="/education/courses",
        tags=["Education — Courses (Global)"],
    )
    # Education — Access Codes
    # TODO: Integrate Wompi payment gateway (wompi.com/es/co)
    # - Plan: Free tier, no monthly fee
    # - Fees: ~2.65% + $700 COP + IVA per card transaction
    # - Supports: Nequi, PSE, credit/debit cards
    # - On successful payment, auto-generate access code and grant access
    # - Current flow: manual Nequi payment → admin generates code → user redeems
    api_v1_router.include_router(
        access_codes_router,
        prefix="/companies/{company_id}/education/access-codes",
        tags=["Education — Access Codes"],
    )
    # Education — Enrollments
    api_v1_router.include_router(
        enrollments_router,
        prefix="/companies/{company_id}/education/enrollments",
        tags=["Education — Enrollments"],
    )
    # Education — Assessment Questions (nested under courses)
    api_v1_router.include_router(
        assessment_questions_router,
        prefix="/companies/{company_id}/education/courses",
        tags=["Education — Assessments"],
    )
    # Education — Assessment Attempts (nested under enrollments)
    api_v1_router.include_router(
        assessment_attempts_router,
        prefix="/companies/{company_id}/education/enrollments",
        tags=["Education — Assessments"],
    )
    # Education — Training Plans
    api_v1_router.include_router(
        training_plans_router,
        prefix="/companies/{company_id}/education/training-plans",
        tags=["Education — Training Plans"],
    )
    api_v1_router.include_router(
        compliance_router, prefix="/compliance", tags=["Compliance"]
    )
    api_v1_router.include_router(
        quality_ops_router, prefix="/quality-ops", tags=["Quality Ops"]
    )

    app.include_router(api_v1_router)
    app.include_router(health_router, prefix="/health", tags=["Health"])


def register_middlewares(app: FastAPI) -> None:
    """Register all middlewares on the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    app.add_middleware(AuthMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:3002",
            "https://quali.tchunza.com",
            "https://company.quali.tchunza.com",
            "https://admin.quali.tchunza.com",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ObservabilityMiddleware)


def create_app() -> FastAPI:
    """Create a new FastAPI application instance.

    Returns:
        FastAPI: The created application instance.
    """
    app = FastAPI(
        title=f"{settings.APP_NAME} - {settings.SCOPE.upper()}",
        version="0.1.0",
        debug=bool(settings.DEBUG),
        lifespan=lifespan,
    )
    register_routes(app)
    register_middlewares(app)
    register_error_handlers(app)
    return app


app = create_app()
