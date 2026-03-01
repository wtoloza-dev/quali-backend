"""E2e tests for DELETE /api/v1/companies/{company_id}."""

BASE_URL = "/api/v1/companies/"


class TestDeleteCompany:
    """Tests for the delete-company endpoint."""

    def test_returns_204_on_success(self, client, company):
        """Deleting an existing company returns 204 with empty body."""
        response = client.delete(f"{BASE_URL}{company['id']}")

        assert response.status_code == 204
        assert response.content == b""

    def test_deleted_company_is_removed(self, client, company):
        """Hard-delete means GET returns 404 after deletion."""
        company_id = company["id"]
        client.delete(f"{BASE_URL}{company_id}")

        response = client.get(f"{BASE_URL}{company_id}")

        assert response.status_code == 404

    def test_returns_404_for_unknown_id(self, client, company):
        """Deleting an already-deleted company returns 404."""
        company_id = company["id"]
        client.delete(f"{BASE_URL}{company_id}")

        response = client.delete(f"{BASE_URL}{company_id}")

        assert response.status_code == 404
        assert response.json()["error_code"] == "COMPANY_NOT_FOUND"
