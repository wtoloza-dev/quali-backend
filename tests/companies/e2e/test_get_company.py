"""E2e tests for GET /api/v1/companies/{company_id}."""

BASE_URL = "/api/v1/companies/"


class TestGetCompany:
    """Tests for the get-company endpoint."""

    def test_returns_200_with_existing_company(self, client, company):
        """Fetching an existing company returns 200 with full data."""
        response = client.get(f"{BASE_URL}{company['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == company["id"]
        assert data["name"] == "Test Company"
        assert data["email"] == "test@company.com"

    def test_returns_404_for_unknown_id(self, client, company):
        """Accessing a deleted company returns 404."""
        company_id = company["id"]
        client.delete(f"{BASE_URL}{company_id}")

        response = client.get(f"{BASE_URL}{company_id}")

        assert response.status_code == 404
        assert response.json()["error_code"] == "COMPANY_NOT_FOUND"
