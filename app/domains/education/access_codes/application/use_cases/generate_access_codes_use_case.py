"""Generate access codes use case."""

import secrets
import string
from datetime import UTC, datetime

from ulid import ULID

from ...domain.entities import AccessCodeData, AccessCodeEntity
from ...domain.ports import AccessCodeRepositoryPort


# Alphanumeric characters excluding ambiguous ones (O/0/I/1)
_ALPHABET = string.ascii_uppercase.replace("O", "").replace("I", "") + string.digits.replace("0", "").replace("1", "")


class GenerateAccessCodesUseCase:
    """Generate a batch of unique access codes for a course.

    Args:
        repository: Port implementation provided by the infrastructure layer.
    """

    def __init__(self, repository: AccessCodeRepositoryPort) -> None:
        """Initialise with the access code repository.

        Args:
            repository: Concrete repository injected by the infrastructure layer.
        """
        self._repository = repository

    async def execute(
        self,
        course_id: str,
        company_id: str,
        quantity: int,
        created_by: str,
    ) -> list[AccessCodeEntity]:
        """Generate and persist N unique access codes.

        Args:
            course_id: ULID of the course these codes unlock.
            company_id: ULID of the company (tenant scope).
            quantity: Number of codes to generate.
            created_by: ULID of the actor generating the codes.

        Returns:
            List of persisted AccessCodeEntity instances.
        """
        now = datetime.now(UTC)
        entities: list[AccessCodeEntity] = []

        for _ in range(quantity):
            code = self._generate_code()
            data = AccessCodeData(
                code=code,
                course_id=course_id,
                company_id=company_id,
            )
            entity = AccessCodeEntity(
                id=str(ULID()),
                code=data.code,
                course_id=data.course_id,
                company_id=data.company_id,
                is_redeemed=False,
                redeemed_by=None,
                redeemed_at=None,
                created_at=now,
                created_by=created_by,
                updated_at=None,
                updated_by=None,
            )
            entities.append(entity)

        return await self._repository.save_batch(entities)

    @staticmethod
    def _generate_code() -> str:
        """Generate a single access code in QUALI-XXXX-XXXX format.

        Uses crypto-random selection to ensure unpredictable codes.

        Returns:
            A string in the format QUALI-XXXX-XXXX.
        """
        segment1 = "".join(secrets.choice(_ALPHABET) for _ in range(4))
        segment2 = "".join(secrets.choice(_ALPHABET) for _ in range(4))
        return f"QUALI-{segment1}-{segment2}"
