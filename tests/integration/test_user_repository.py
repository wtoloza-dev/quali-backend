"""Integration tests for UserRepository against a real PostgreSQL container."""

import pytest

from app.domains.users.domain.entities import UserEntity
from app.domains.users.infrastructure.repositories.user_repository import UserRepository


pytestmark = pytest.mark.integration

USER_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAU"
CREATED_BY = "01ARZ3NDEKTSV4RRFFQ69G5FAA"


def _make_entity(user_id: str = USER_ID, email: str = "jane@example.com") -> UserEntity:
    from datetime import UTC, datetime
    now = datetime.now(UTC)
    return UserEntity(
        id=user_id,
        first_name="Jane",
        last_name="Doe",
        email=email,
        created_at=now,
        created_by=CREATED_BY,
        updated_at=now,
        updated_by=None,
    )


class TestUserRepository:
    async def test_save_and_get_by_id(self, session):
        repo = UserRepository(session=session)
        entity = _make_entity()

        saved = await repo.save(entity)
        found = await repo.get_by_id(USER_ID)

        assert found is not None
        assert found.id == saved.id
        assert found.email == "jane@example.com"

    async def test_get_by_id_returns_none_for_unknown(self, session):
        repo = UserRepository(session=session)

        result = await repo.get_by_id("nonexistent-id")

        assert result is None

    async def test_get_by_email(self, session):
        repo = UserRepository(session=session)
        await repo.save(_make_entity())

        found = await repo.get_by_email("jane@example.com")

        assert found is not None
        assert found.id == USER_ID

    async def test_get_by_email_returns_none_for_unknown(self, session):
        repo = UserRepository(session=session)

        result = await repo.get_by_email("ghost@example.com")

        assert result is None

    async def test_get_by_id_excludes_soft_deleted(self, session):
        repo = UserRepository(session=session)
        await repo.save(_make_entity())
        await repo.delete(USER_ID, deleted_by=CREATED_BY)

        found = await repo.get_by_id(USER_ID)

        assert found is None

    async def test_get_by_email_excludes_soft_deleted(self, session):
        repo = UserRepository(session=session)
        await repo.save(_make_entity())
        await repo.delete(USER_ID, deleted_by=CREATED_BY)

        found = await repo.get_by_email("jane@example.com")

        assert found is None

    async def test_update_persists_changes(self, session):
        repo = UserRepository(session=session)
        entity = await repo.save(_make_entity())

        updated = entity.model_copy(update={"first_name": "Janet"})
        await repo.update(updated)

        found = await repo.get_by_id(USER_ID)
        assert found.first_name == "Janet"
