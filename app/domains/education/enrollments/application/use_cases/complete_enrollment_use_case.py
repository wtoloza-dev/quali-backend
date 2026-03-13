"""Complete enrollment use case."""

from datetime import UTC, datetime, timedelta

from ulid import ULID

from app.domains.certification.domain.entities import CertificateEntity
from app.domains.certification.domain.ports import CertificateRepositoryPort
from app.domains.education.assessments.domain.ports import AttemptRepositoryPort
from app.domains.education.courses.domain.ports import (
    CourseRepositoryPort,
    ModuleRepositoryPort,
)
from app.shared.exceptions import ForbiddenException, NotFoundException

from ...domain.entities import EnrollmentEntity
from ...domain.enums import EnrollmentStatus
from ...domain.exceptions import EnrollmentNotFoundException
from ...domain.ports import EnrollmentRepositoryPort


class CompleteEnrollmentUseCase:
    """Validate all modules are passed, complete the enrollment, and issue a certificate.

    This use case orchestrates across enrollment, assessment, course, and
    certification domains to atomically complete a course and generate
    the corresponding certificate.

    Args:
        enrollment_repository: Port for enrollment persistence.
        attempt_repository: Port for reading assessment attempts.
        course_repository: Port for reading course data.
        module_repository: Port for reading course modules.
        certificate_repository: Port for certificate persistence.
    """

    def __init__(
        self,
        enrollment_repository: EnrollmentRepositoryPort,
        attempt_repository: AttemptRepositoryPort,
        course_repository: CourseRepositoryPort,
        module_repository: ModuleRepositoryPort,
        certificate_repository: CertificateRepositoryPort,
    ) -> None:
        """Initialise with required repository ports.

        Args:
            enrollment_repository: Enrollment persistence.
            attempt_repository: Assessment attempt queries.
            course_repository: Course data queries.
            module_repository: Module data queries.
            certificate_repository: Certificate persistence.
        """
        self._enrollments = enrollment_repository
        self._attempts = attempt_repository
        self._courses = course_repository
        self._modules = module_repository
        self._certificates = certificate_repository

    async def execute(
        self,
        enrollment_id: str,
        completed_by: str,
    ) -> tuple[EnrollmentEntity, CertificateEntity]:
        """Complete an enrollment and issue a certificate.

        Validates that every module in the course has at least one passing
        attempt, transitions the enrollment to COMPLETED, and creates a
        certificate for the user.

        Args:
            enrollment_id: ULID of the enrollment to complete.
            completed_by: Firebase UID of the authenticated user.

        Returns:
            Tuple of (updated EnrollmentEntity, issued CertificateEntity).

        Raises:
            EnrollmentNotFoundException: If the enrollment does not exist.
            ForbiddenException: If the user does not own the enrollment,
                enrollment is already completed, or not all modules are passed.
            NotFoundException: If the course does not exist.
        """
        enrollment = await self._enrollments.get_by_id(enrollment_id)
        if enrollment is None:
            raise EnrollmentNotFoundException(enrollment_id)

        if enrollment.user_id != completed_by:
            raise ForbiddenException(
                message="You do not have access to this enrollment.",
                context={"enrollment_id": enrollment_id},
                error_code="ENROLLMENT_ACCESS_DENIED",
            )

        if enrollment.status == EnrollmentStatus.COMPLETED:
            raise ForbiddenException(
                message="Enrollment is already completed.",
                context={"enrollment_id": enrollment_id},
                error_code="ENROLLMENT_ALREADY_COMPLETED",
            )

        course = await self._courses.get_by_id(enrollment.course_id)
        if course is None:
            raise NotFoundException(
                message="Course not found.",
                context={"course_id": enrollment.course_id},
                error_code="COURSE_NOT_FOUND",
            )

        modules = await self._modules.list_by_course(enrollment.course_id)
        if not modules:
            raise ForbiddenException(
                message="Course has no modules to complete.",
                context={"course_id": enrollment.course_id},
                error_code="COURSE_NO_MODULES",
            )

        attempts = await self._attempts.list_by_enrollment(enrollment_id)
        passed_module_ids = {a.module_id for a in attempts if a.passed and a.module_id}
        all_module_ids = {m.id for m in modules}
        missing = all_module_ids - passed_module_ids

        if missing:
            raise ForbiddenException(
                message="Not all modules have been passed.",
                context={"missing_module_ids": sorted(missing)},
                error_code="MODULES_NOT_COMPLETED",
            )

        now = datetime.now(UTC)

        updated_enrollment = enrollment.model_copy(
            update={
                "status": EnrollmentStatus.COMPLETED,
                "completed_at": now,
                "updated_by": completed_by,
            }
        )
        updated_enrollment = await self._enrollments.update(updated_enrollment)

        expires_at = (
            now + timedelta(days=course.validity_days) if course.validity_days else None
        )

        certificate = CertificateEntity(
            id=str(ULID()),
            token=str(ULID()),
            company_id=course.company_id,
            recipient_id=enrollment.user_id,
            title=course.title,
            description=course.description,
            issued_at=now,
            expires_at=expires_at,
            revoked_at=None,
            revoked_by=None,
            revoked_reason=None,
            created_at=now,
            created_by=completed_by,
            updated_at=None,
            updated_by=None,
        )
        saved_certificate = await self._certificates.save(certificate)

        return updated_enrollment, saved_certificate
