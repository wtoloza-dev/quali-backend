"""Redeem access code use case."""

from datetime import UTC, datetime

from ulid import ULID

from app.domains.education.enrollments.domain.entities import EnrollmentEntity
from app.domains.education.enrollments.domain.enums import AccessType
from app.domains.education.enrollments.domain.ports import EnrollmentRepositoryPort

from ...domain.entities import AccessCodeEntity
from ...domain.exceptions import (
    AccessCodeAlreadyRedeemedException,
    AccessCodeNotFoundException,
)
from ...domain.ports import AccessCodeRepositoryPort


class RedeemAccessCodeUseCase:
    """Validate and redeem an access code, granting full course access.

    On redemption, upgrades the user's enrollment to FULL access. If the
    user has no enrollment yet, creates one with FULL access.

    Args:
        repository: Port implementation provided by the infrastructure layer.
        enrollment_repository: Enrollment port to look up and update enrollments.
    """

    def __init__(
        self,
        repository: AccessCodeRepositoryPort,
        enrollment_repository: EnrollmentRepositoryPort,
    ) -> None:
        """Initialise with the access code and enrollment repositories.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
            enrollment_repository: Enrollment repository for access upgrades.
        """
        self._repository = repository
        self._enrollment_repository = enrollment_repository

    async def execute(
        self,
        code: str,
        user_id: str,
    ) -> AccessCodeEntity:
        """Redeem an access code and grant full course access to the user.

        Args:
            code: The access code string to redeem.
            user_id: ULID of the user redeeming the code.

        Returns:
            AccessCodeEntity: The redeemed access code entity.

        Raises:
            AccessCodeNotFoundException: If the code does not exist.
            AccessCodeAlreadyRedeemedException: If the code was already used.
        """
        entity = await self._repository.get_by_code(code)
        if entity is None:
            raise AccessCodeNotFoundException(code=code)

        if entity.is_redeemed:
            raise AccessCodeAlreadyRedeemedException(code=code)

        now = datetime.now(UTC)

        # Upgrade or create enrollment with FULL access.
        enrollment = await self._enrollment_repository.get_by_user_and_course(
            user_id=user_id,
            course_id=entity.course_id,
        )
        if enrollment is not None:
            upgraded = enrollment.model_copy(
                update={
                    "access_type": AccessType.FULL,
                    "start_date": now,
                    "updated_by": user_id,
                }
            )
            enrollment = await self._enrollment_repository.update(upgraded)
        else:
            enrollment = EnrollmentEntity(
                id=str(ULID()),
                user_id=user_id,
                course_id=entity.course_id,
                is_mandatory=False,
                access_type=AccessType.FULL,
                start_date=now,
                enrolled_at=now,
                created_at=now,
                created_by=user_id,
                updated_at=None,
                updated_by=None,
            )
            enrollment = await self._enrollment_repository.save(enrollment)

        redeemed_entity = AccessCodeEntity(
            id=entity.id,
            code=entity.code,
            course_id=entity.course_id,
            is_redeemed=True,
            redeemed_by=user_id,
            redeemed_at=now,
            enrollment_id=enrollment.id,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=user_id,
        )
        return await self._repository.update(redeemed_entity)
