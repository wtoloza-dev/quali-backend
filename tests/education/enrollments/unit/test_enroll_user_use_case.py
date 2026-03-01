"""Unit tests for EnrollUserUseCase."""

from app.domains.education.enrollments.application.use_cases import EnrollUserUseCase
from app.domains.education.enrollments.domain.entities import (
    EnrollmentData,
    EnrollmentEntity,
)
from app.domains.education.enrollments.domain.enums import EnrollmentStatus


COMPANY_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAC"
USER_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAU"
COURSE_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAR"
CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAA"


class FakeEnrollmentRepository:
    """In-memory enrollment repository."""

    def __init__(self) -> None:
        self._store: dict[str, EnrollmentEntity] = {}

    async def save(self, entity: EnrollmentEntity) -> EnrollmentEntity:
        self._store[entity.id] = entity
        return entity

    async def get_by_id(self, enrollment_id: str) -> EnrollmentEntity | None:
        return self._store.get(enrollment_id)

    async def get_by_id_and_company(self, enrollment_id: str, company_id: str):
        entity = self._store.get(enrollment_id)
        if entity is None or entity.company_id != company_id:
            return None
        return entity


    async def get_active_enrollment(self, user_id: str, course_id: str):
        return next(
            (
                e
                for e in self._store.values()
                if e.user_id == user_id
                and e.course_id == course_id
                and e.status
                in (EnrollmentStatus.NOT_STARTED, EnrollmentStatus.IN_PROGRESS)
            ),
            None,
        )

    async def update(self, entity: EnrollmentEntity) -> EnrollmentEntity:
        self._store[entity.id] = entity
        return entity

    async def delete(self, enrollment_id: str, deleted_by: str) -> None:
        self._store.pop(enrollment_id, None)

    async def list_by_company(self, company_id: str, page: int, page_size: int):
        items = [e for e in self._store.values() if e.company_id == company_id]
        offset = (page - 1) * page_size
        return items[offset : offset + page_size], len(items)


def _valid_data(**kwargs) -> EnrollmentData:
    return EnrollmentData(
        user_id=kwargs.get("user_id", USER_ID),
        course_id=kwargs.get("course_id", COURSE_ID),
        company_id=kwargs.get("company_id", COMPANY_ID),
        is_mandatory=kwargs.get("is_mandatory", False),
    )


class TestEnrollUserUseCase:
    async def test_creates_enrollment_successfully(self):
        repo = FakeEnrollmentRepository()
        use_case = EnrollUserUseCase(repository=repo)

        result = await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

        assert result.id is not None
        assert result.user_id == USER_ID
        assert result.course_id == COURSE_ID
        assert result.company_id == COMPANY_ID
        assert result.created_by == CREATED_BY

    async def test_initial_status_is_not_started(self):
        repo = FakeEnrollmentRepository()
        use_case = EnrollUserUseCase(repository=repo)

        result = await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

        assert result.status == EnrollmentStatus.NOT_STARTED

    async def test_enrolled_at_is_set(self):
        repo = FakeEnrollmentRepository()
        use_case = EnrollUserUseCase(repository=repo)

        result = await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

        assert result.enrolled_at is not None

    async def test_completed_at_is_none_on_creation(self):
        repo = FakeEnrollmentRepository()
        use_case = EnrollUserUseCase(repository=repo)

        result = await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

        assert result.completed_at is None

    async def test_is_mandatory_flag_is_preserved(self):
        repo = FakeEnrollmentRepository()
        use_case = EnrollUserUseCase(repository=repo)

        result = await use_case.execute(
            data=_valid_data(is_mandatory=True), created_by=CREATED_BY
        )

        assert result.is_mandatory is True
