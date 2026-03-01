"""Shared fixtures for the users domain tests."""

from datetime import UTC, datetime

import pytest

from app.domains.users.domain.entities import UserEntity
from app.domains.users.domain.ports import UserRepositoryPort


class FakeUserRepository:
    """In-memory implementation of UserRepositoryPort for testing.

    Stores entities in a dict keyed by ULID. Used via dependency
    override — never patches source code.
    """

    def __init__(self) -> None:
        self._store: dict[str, UserEntity] = {}

    async def save(self, entity: UserEntity) -> UserEntity:
        self._store[entity.id] = entity
        return entity

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        return self._store.get(user_id)

    async def get_by_email(self, email: str) -> UserEntity | None:
        return next(
            (e for e in self._store.values() if e.email == email),
            None,
        )

    async def update(self, entity: UserEntity) -> UserEntity:
        self._store[entity.id] = entity
        return entity

    async def delete(self, user_id: str, deleted_by: str) -> None:
        self._store.pop(user_id, None)


# Verify FakeUserRepository satisfies the protocol at import time
_: UserRepositoryPort = FakeUserRepository()  # type: ignore[assignment]


@pytest.fixture
def fake_user_repository() -> FakeUserRepository:
    """Fresh in-memory repository for each test."""
    return FakeUserRepository()


@pytest.fixture
def user_entity() -> UserEntity:
    """A fully populated UserEntity for use in assertions."""
    now = datetime.now(UTC)
    return UserEntity(
        id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        created_at=now,
        created_by="01ARZ3NDEKTSV4RRFFQ69G5FAB",
        updated_at=now,
        updated_by=None,
    )
