"""E2e tests for POST /api/v1/companies/{company_id}/education/training-plans/."""

VALID_PAYLOAD = {
    "year": 2026,
    "title": "Annual Safety Training",
}


class TestCreateTrainingPlan:
    """Verify training plan creation."""

    def test_returns_201_with_plan(self, client, company):
        """Create a training plan and verify the response."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"

        response = client.post(url, json=VALID_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["year"] == 2026
        assert data["title"] == "Annual Safety Training"
        assert data["company_id"] == company["id"]
        assert data["status"] == "draft"
        assert "id" in data

    def test_initial_status_is_draft(self, client, company):
        """A new training plan should start in draft status."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"

        response = client.post(url, json=VALID_PAYLOAD)

        assert response.json()["status"] == "draft"

    def test_missing_required_field_returns_422(self, client, company):
        """Missing title should return 422."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"

        response = client.post(url, json={"year": 2026})

        assert response.status_code == 422
