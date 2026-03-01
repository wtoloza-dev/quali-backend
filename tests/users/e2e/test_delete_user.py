"""E2e tests for DELETE /api/v1/users/{user_id}."""


BASE_URL = "/api/v1/users/"
TEST_USER_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAU"


class TestDeleteUser:
    def test_returns_204_on_success(self, client):
        client.post("/api/v1/users/me")

        response = client.delete(f"{BASE_URL}{TEST_USER_ID}")

        assert response.status_code == 204

    def test_deleted_user_is_invisible_to_get(self, client):
        client.post("/api/v1/users/me")
        client.delete(f"{BASE_URL}{TEST_USER_ID}")

        response = client.get(f"{BASE_URL}{TEST_USER_ID}")

        assert response.status_code == 404

    def test_already_deleted_returns_404(self, client):
        client.post("/api/v1/users/me")
        client.delete(f"{BASE_URL}{TEST_USER_ID}")

        response = client.delete(f"{BASE_URL}{TEST_USER_ID}")

        assert response.status_code == 404
        assert response.json()["error_code"] == "USER_NOT_FOUND"

    def test_unknown_id_returns_404(self, client):
        response = client.delete(f"{BASE_URL}{TEST_USER_ID}")

        assert response.status_code == 404
        assert response.json()["error_code"] == "USER_NOT_FOUND"
