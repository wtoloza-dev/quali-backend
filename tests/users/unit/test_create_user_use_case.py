"""Unit tests for CreateUserUseCase."""

import pytest

from app.domains.users.application.use_cases import CreateUserUseCase
from app.domains.users.domain.entities import UserData, UserEntity
from app.domains.users.domain.exceptions import UserEmailTakenException


CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAU"


def _valid_data(email: str = "jane@example.com") -> UserData:
    return UserData(first_name="Jane", last_name="Doe", email=email)


class FakeUserRepository:
    def __init__(self):
        self._store: dict[str, UserEntity] = {}

    async def save(self, entity: UserEntity) -> UserEntity:
        self._store[entity.id] = entity
        return entity

    async def get_by_id(self, user_id): return self._store.get(user_id)
    async def get_by_email(self, email):
        return next((e for e in self._store.values() if e.email == email), None)
    async def update(self, entity): return entity
    async def delete(self, user_id, deleted_by): self._store.pop(user_id, None)


class TestCreateUserUseCase:
    async def test_creates_user_successfully(self):
        repo = FakeUserRepository()
        use_case = CreateUserUseCase(repository=repo)

        result = await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

        assert result.id is not None
        assert result.email == "jane@example.com"
        assert result.created_by == CREATED_BY

    async def test_raises_when_email_is_taken(self):
        repo = FakeUserRepository()
        use_case = CreateUserUseCase(repository=repo)
        await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

        with pytest.raises(UserEmailTakenException):
            await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

    async def test_uses_provided_user_id(self):
        repo = FakeUserRepository()
        use_case = CreateUserUseCase(repository=repo)
        explicit_id = "01ARZ3NDEKTSV4RRFFQ69G5FAX"

        result = await use_case.execute(
            data=_valid_data(), created_by=CREATED_BY, user_id=explicit_id
        )

        assert result.id == explicit_id

    async def test_generates_id_when_not_provided(self):
        repo = FakeUserRepository()
        use_case = CreateUserUseCase(repository=repo)

        result = await use_case.execute(data=_valid_data(), created_by=CREATED_BY)

        assert len(result.id) > 0

    async def test_self_registration_created_by_equals_id(self):
        repo = FakeUserRepository()
        use_case = CreateUserUseCase(repository=repo)
        new_id = "01ARZ3NDEKTSV4RRFFQ69G5FAX"

        result = await use_case.execute(
            data=_valid_data(), created_by=new_id, user_id=new_id
        )

        assert result.created_by == result.id
