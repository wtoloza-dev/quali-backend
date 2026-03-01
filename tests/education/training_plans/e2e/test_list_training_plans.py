"""E2e tests for GET /api/v1/companies/{company_id}/education/training-plans/."""

VALID_PAYLOAD = {"year": 2026, "title": "Plan"}


class TestListTrainingPlans:
    """Verify training plan listing and pagination."""

    def test_returns_empty_list(self, client, company):
        """No training plans should return an empty paginated result."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"

        response = client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_returns_created_plan(self, client, company):
        """Creating a plan should make it appear in the list."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"
        client.post(url, json=VALID_PAYLOAD)

        response = client.get(url)

        assert response.json()["total"] == 1

    def test_pagination_fields_present(self, client, company):
        """Paginated response must contain standard pagination fields."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"

        response = client.get(url)

        data = response.json()
        assert "page" in data
        assert "page_size" in data
        assert "total" in data
        assert "items" in data
