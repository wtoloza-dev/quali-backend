"""Unit tests for UpdateEnrollmentStatusUseCase."""

from datetime import UTC, datetime

import pytest

from app.domains.education.enrollments.application.use_cases import (
    UpdateEnrollmentStatusUseCase,
)
from app.domains.education.enrollments.domain.entities import EnrollmentEntity
from app.domains.education.enrollments.domain.enums import (
    AccessType,
    EnrollmentStatus,
)
from app.domains.education.enrollments.domain.exceptions import (
    EnrollmentNotFoundException,
    InvalidStatusTransitionException,
)


ENROLLMENT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAE"
UPDATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAA"


def _make_enrollment(**kwargs) -> EnrollmentEntity:
    now = datetime.now(UTC)
    return EnrollmentEntity(
        id=kwargs.get("id", ENROLLMENT_ID),
        user_id="01ARZ3NDEKTSV4RRFFQ69G5FAU",
        course_id="01ARZ3NDEKTSV4RRFFQ69G5FAR",
        is_mandatory=False,
        status=kwargs.get("status", EnrollmentStatus.NOT_STARTED),
        access_type=AccessType.PREVIEW,
        enrolled_at=now,
        completed_at=kwargs.get("completed_at"),
        start_date=None,
        end_date=None,
        created_at=now,
        created_by="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        updated_at=now,
        updated_by=None,
    )


class FakeEnrollmentRepository:
    def __init__(self, initial: EnrollmentEntity | None = None) -> None:
        self._store: dict[str, EnrollmentEntity] = {}
        if initial:
            self._store[initial.id] = initial

    async def get_by_id(self, enrollment_id: str) -> EnrollmentEntity | None:
        return self._store.get(enrollment_id)

    async def update(self, entity: EnrollmentEntity) -> EnrollmentEntity:
        self._store[entity.id] = entity
        return entity

    async def save(self, entity: EnrollmentEntity) -> EnrollmentEntity:
        self._store[entity.id] = entity
        return entity

    async def get_active_enrollment(self, user_id, course_id):
        return None

    async def get_by_user_and_course(self, user_id, course_id):
        return None

    async def delete(self, enrollment_id, deleted_by):
        self._store.pop(enrollment_id, None)

    async def list_by_user(self, user_id, page, page_size):
        return [], 0


class TestUpdateEnrollmentStatusUseCase:
    async def test_updates_status_successfully(self):
        enrollment = _make_enrollment()
        repo = FakeEnrollmentRepository(initial=enrollment)
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        result = await use_case.execute(
            enrollment_id=ENROLLMENT_ID,
            status=EnrollmentStatus.IN_PROGRESS,
            updated_by=UPDATED_BY,
        )

        assert result.status == EnrollmentStatus.IN_PROGRESS
        assert result.updated_by == UPDATED_BY

    async def test_sets_completed_at_when_completed(self):
        enrollment = _make_enrollment(status=EnrollmentStatus.IN_PROGRESS)
        repo = FakeEnrollmentRepository(initial=enrollment)
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        result = await use_case.execute(
            enrollment_id=ENROLLMENT_ID,
            status=EnrollmentStatus.COMPLETED,
            updated_by=UPDATED_BY,
        )

        assert result.completed_at is not None

    async def test_sets_completed_at_when_failed(self):
        enrollment = _make_enrollment(status=EnrollmentStatus.IN_PROGRESS)
        repo = FakeEnrollmentRepository(initial=enrollment)
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        result = await use_case.execute(
            enrollment_id=ENROLLMENT_ID,
            status=EnrollmentStatus.FAILED,
            updated_by=UPDATED_BY,
        )

        assert result.completed_at is not None

    async def test_does_not_overwrite_existing_completed_at(self):
        # Edge case: in_progress enrollment that already has completed_at set.
        existing_completed_at = datetime(2025, 1, 1, tzinfo=UTC)
        enrollment = _make_enrollment(
            status=EnrollmentStatus.IN_PROGRESS,
            completed_at=existing_completed_at,
        )
        repo = FakeEnrollmentRepository(initial=enrollment)
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        result = await use_case.execute(
            enrollment_id=ENROLLMENT_ID,
            status=EnrollmentStatus.COMPLETED,
            updated_by=UPDATED_BY,
        )

        assert result.completed_at == existing_completed_at

    async def test_does_not_set_completed_at_for_in_progress(self):
        enrollment = _make_enrollment()
        repo = FakeEnrollmentRepository(initial=enrollment)
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        result = await use_case.execute(
            enrollment_id=ENROLLMENT_ID,
            status=EnrollmentStatus.IN_PROGRESS,
            updated_by=UPDATED_BY,
        )

        assert result.completed_at is None

    async def test_raises_when_enrollment_not_found(self):
        repo = FakeEnrollmentRepository()
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        with pytest.raises(EnrollmentNotFoundException):
            await use_case.execute(
                enrollment_id="nonexistent",
                status=EnrollmentStatus.COMPLETED,
                updated_by=UPDATED_BY,
            )

    async def test_raises_on_invalid_transition_from_not_started_to_completed(self):
        enrollment = _make_enrollment(status=EnrollmentStatus.NOT_STARTED)
        repo = FakeEnrollmentRepository(initial=enrollment)
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        with pytest.raises(InvalidStatusTransitionException):
            await use_case.execute(
                enrollment_id=ENROLLMENT_ID,
                status=EnrollmentStatus.COMPLETED,
                updated_by=UPDATED_BY,
            )

    async def test_raises_on_invalid_transition_from_completed(self):
        enrollment = _make_enrollment(status=EnrollmentStatus.COMPLETED)
        repo = FakeEnrollmentRepository(initial=enrollment)
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        with pytest.raises(InvalidStatusTransitionException):
            await use_case.execute(
                enrollment_id=ENROLLMENT_ID,
                status=EnrollmentStatus.IN_PROGRESS,
                updated_by=UPDATED_BY,
            )

    async def test_allows_failed_to_not_started_reset(self):
        enrollment = _make_enrollment(status=EnrollmentStatus.FAILED)
        repo = FakeEnrollmentRepository(initial=enrollment)
        use_case = UpdateEnrollmentStatusUseCase(repository=repo)

        result = await use_case.execute(
            enrollment_id=ENROLLMENT_ID,
            status=EnrollmentStatus.NOT_STARTED,
            updated_by=UPDATED_BY,
        )

        assert result.status == EnrollmentStatus.NOT_STARTED
