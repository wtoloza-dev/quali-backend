"""E2e tests for PATCH /api/v1/companies/{company_id}/education/training-plans/{plan_id}."""

VALID_PAYLOAD = {"year": 2026, "title": "Original Title"}


class TestUpdateTrainingPlan:
    """Verify training plan updates."""

    def test_updates_title(self, client, company):
        """Updating the title should reflect in the response."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"
        created = client.post(url, json=VALID_PAYLOAD).json()

        response = client.patch(
            f"{url}{created['id']}",
            json={"title": "Updated Title"},
        )

        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    def test_updates_status(self, client, company):
        """Updating the status should reflect in the response."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"
        created = client.post(url, json=VALID_PAYLOAD).json()

        response = client.patch(
            f"{url}{created['id']}",
            json={"status": "active"},
        )

        assert response.status_code == 200
        assert response.json()["status"] == "active"

    def test_returns_404_for_unknown_plan(self, client, company):
        """Updating an unknown plan should return 404."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"

        response = client.patch(
            f"{url}nonexistent-id",
            json={"title": "New Title"},
        )

        assert response.status_code == 404
