"""E2e tests for GET /api/v1/users/{user_id}."""


BASE_URL = "/api/v1/users/"
TEST_USER_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAU"


class TestGetUser:
    def test_returns_200_with_user_data(self, client):
        client.post("/api/v1/users/me")

        response = client.get(f"{BASE_URL}{TEST_USER_ID}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == TEST_USER_ID
        assert data["email"] == "test@example.com"

    def test_unknown_id_returns_404(self, client):
        response = client.get(f"{BASE_URL}{TEST_USER_ID}")

        assert response.status_code == 404
        assert response.json()["error_code"] == "USER_NOT_FOUND"

    def test_deleted_user_returns_404(self, client):
        client.post("/api/v1/users/me")
        client.delete(f"{BASE_URL}{TEST_USER_ID}")

        response = client.get(f"{BASE_URL}{TEST_USER_ID}")

        assert response.status_code == 404
        assert response.json()["error_code"] == "USER_NOT_FOUND"
