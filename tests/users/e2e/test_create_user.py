"""E2e tests for POST /api/v1/users/me."""


class TestCreateUser:
    def test_returns_201_with_private_response(self, client):
        response = client.post("/api/v1/users/me")

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_response_includes_audit_fields(self, client):
        response = client.post("/api/v1/users/me")

        data = response.json()
        assert "created_at" in data
        assert "created_by" in data
        assert "updated_at" in data

    def test_duplicate_returns_200(self, client):
        client.post("/api/v1/users/me")
        response = client.post("/api/v1/users/me")

        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
