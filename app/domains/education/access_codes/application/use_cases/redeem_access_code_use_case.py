"""Redeem access code use case."""

from datetime import UTC, datetime

from app.domains.education.courses.application.use_cases import GrantCourseAccessUseCase
from app.domains.education.courses.domain.entities import CourseAccessData
from app.domains.education.courses.domain.enums import AccessType

from ...domain.entities import AccessCodeEntity
from ...domain.exceptions import (
    AccessCodeAlreadyRedeemedException,
    AccessCodeNotFoundException,
)
from ...domain.ports import AccessCodeRepositoryPort


class RedeemAccessCodeUseCase:
    """Validate and redeem an access code, granting course access.

    Args:
        repository: Port implementation provided by the infrastructure layer.
        grant_access_use_case: Use case to grant course access upon redemption.
    """

    def __init__(
        self,
        repository: AccessCodeRepositoryPort,
        grant_access_use_case: GrantCourseAccessUseCase,
    ) -> None:
        """Initialise with the access code repository and grant access use case.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
            grant_access_use_case: Use case to insert course access records.
        """
        self._repository = repository
        self._grant_access_use_case = grant_access_use_case

    async def execute(
        self,
        code: str,
        user_id: str,
    ) -> AccessCodeEntity:
        """Redeem an access code and grant course access to the user.

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
        redeemed_entity = AccessCodeEntity(
            id=entity.id,
            code=entity.code,
            course_id=entity.course_id,
            company_id=entity.company_id,
            is_redeemed=True,
            redeemed_by=user_id,
            redeemed_at=now,
            created_at=entity.created_at,
            created_by=entity.created_by,
            updated_at=entity.updated_at,
            updated_by=user_id,
        )
        updated = await self._repository.update(redeemed_entity)

        access_data = CourseAccessData(
            user_id=user_id,
            course_id=entity.course_id,
            access_type=AccessType.PURCHASE,
            expires_at=None,
        )
        await self._grant_access_use_case.execute(
            data=access_data,
            created_by=user_id,
        )

        return updated
