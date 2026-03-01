"""E2e tests for PATCH /api/v1/users/{user_id}."""


BASE_URL = "/api/v1/users/"
TEST_USER_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAU"


class TestUpdateUser:
    def test_returns_200_with_updated_fields(self, client):
        client.post("/api/v1/users/me")

        response = client.patch(
            f"{BASE_URL}{TEST_USER_ID}",
            json={"first_name": "Janet"},
        )

        assert response.status_code == 200
        assert response.json()["first_name"] == "Janet"
        assert response.json()["last_name"] == ""

    def test_email_is_ignored_if_sent(self, client):
        """Email is not in the update schema so it is silently ignored."""
        client.post("/api/v1/users/me")

        response = client.patch(
            f"{BASE_URL}{TEST_USER_ID}",
            json={"email": "new@example.com", "first_name": "Janet"},
        )

        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_partial_update_preserves_other_fields(self, client):
        client.post("/api/v1/users/me")
        client.patch(f"{BASE_URL}{TEST_USER_ID}", json={"first_name": "Janet"})

        response = client.get(f"{BASE_URL}{TEST_USER_ID}")

        assert response.json()["last_name"] == ""
        assert response.json()["email"] == "test@example.com"

    def test_returns_404_for_unknown_id(self, client):
        response = client.patch(
            f"{BASE_URL}{TEST_USER_ID}", json={"first_name": "X"}
        )

        assert response.status_code == 404
        assert response.json()["error_code"] == "USER_NOT_FOUND"
