"""E2e tests for PATCH /api/v1/companies/{company_id}."""

BASE_URL = "/api/v1/companies/"


class TestUpdateCompany:
    """Tests for the update-company endpoint."""

    def test_returns_200_with_updated_fields(self, client, company):
        """Patching a field returns 200 with the updated value."""
        response = client.patch(
            f"{BASE_URL}{company['id']}",
            json={"name": "Acme Corporation"},
        )

        assert response.status_code == 200
        assert response.json()["name"] == "Acme Corporation"
        assert response.json()["slug"] == "test-company"  # immutable

    def test_slug_is_ignored_if_sent(self, client, company):
        """Slug is not in the schema so it is silently ignored."""
        response = client.patch(
            f"{BASE_URL}{company['id']}",
            json={"slug": "new-slug", "name": "New Name"},
        )

        assert response.status_code == 200
        assert response.json()["slug"] == "test-company"  # unchanged

    def test_partial_update_preserves_other_fields(self, client, company):
        """Updating one field does not affect other fields."""
        client.patch(f"{BASE_URL}{company['id']}", json={"name": "New Name"})
        response = client.get(f"{BASE_URL}{company['id']}")

        assert response.json()["email"] == "test@company.com"

    def test_returns_404_for_unknown_id(self, client, company):
        """Updating a deleted company returns 404."""
        company_id = company["id"]
        client.delete(f"{BASE_URL}{company_id}")

        response = client.patch(f"{BASE_URL}{company_id}", json={"name": "X"})

        assert response.status_code == 404
        assert response.json()["error_code"] == "COMPANY_NOT_FOUND"
