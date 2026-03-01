"""E2e tests for GET /api/v1/companies/{company_id}/education/training-plans/{plan_id}."""

VALID_PAYLOAD = {"year": 2026, "title": "Test Plan"}


class TestGetTrainingPlan:
    """Verify single training plan retrieval."""

    def test_returns_plan_by_id(self, client, company):
        """Fetch a training plan by its ID."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"
        created = client.post(url, json=VALID_PAYLOAD).json()

        response = client.get(f"{url}{created['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created["id"]
        assert data["title"] == "Test Plan"

    def test_returns_404_for_unknown_id(self, client, company):
        """Unknown plan ID should return 404."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"

        response = client.get(f"{url}nonexistent-id")

        assert response.status_code == 404
