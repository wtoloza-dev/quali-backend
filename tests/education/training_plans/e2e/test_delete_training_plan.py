"""E2e tests for DELETE /api/v1/companies/{company_id}/education/training-plans/{plan_id}."""

VALID_PAYLOAD = {"year": 2026, "title": "Plan to delete"}


class TestDeleteTrainingPlan:
    """Verify training plan deletion."""

    def test_deletes_plan_successfully(self, client, company):
        """Deleting a plan should return 204."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"
        created = client.post(url, json=VALID_PAYLOAD).json()

        response = client.delete(f"{url}{created['id']}")

        assert response.status_code == 204

    def test_plan_not_in_list_after_delete(self, client, company):
        """A deleted plan should not appear in the list."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"
        created = client.post(url, json=VALID_PAYLOAD).json()
        client.delete(f"{url}{created['id']}")

        response = client.get(url)

        assert response.json()["total"] == 0

    def test_returns_404_for_unknown_plan(self, client, company):
        """Deleting an unknown plan should return 404."""
        url = f"/api/v1/companies/{company['id']}/education/training-plans/"

        response = client.delete(f"{url}nonexistent-id")

        assert response.status_code == 404
