"""Unit tests for UserMapper."""

from app.domains.users.presentation.mappers.user_mapper import UserMapper


class TestToPublicResponse:
    def test_returns_public_fields(self, user_entity):
        result = UserMapper.to_public_response(user_entity)

        assert result.id == user_entity.id
        assert result.first_name == user_entity.first_name
        assert result.last_name == user_entity.last_name
        assert result.created_at == user_entity.created_at

    def test_excludes_pii_fields(self, user_entity):
        result = UserMapper.to_public_response(user_entity)

        assert not hasattr(result, "email")

    def test_excludes_audit_fields(self, user_entity):
        result = UserMapper.to_public_response(user_entity)

        assert not hasattr(result, "created_by")
        assert not hasattr(result, "updated_at")


class TestToPrivateResponse:
    def test_returns_all_fields(self, user_entity):
        result = UserMapper.to_private_response(user_entity)

        assert result.id == user_entity.id
        assert result.first_name == user_entity.first_name
        assert result.last_name == user_entity.last_name
        assert result.email == user_entity.email
        assert result.created_at == user_entity.created_at
        assert result.created_by == user_entity.created_by
        assert result.updated_at == user_entity.updated_at
        assert result.updated_by == user_entity.updated_by

    def test_includes_email(self, user_entity):
        result = UserMapper.to_private_response(user_entity)

        assert result.email == "jane.doe@example.com"

    def test_audit_fields_none_when_not_set(self, user_entity):
        result = UserMapper.to_private_response(user_entity)

        assert result.updated_by is None
