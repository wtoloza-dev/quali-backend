"""E2e tests for GET /api/v1/companies/{company_id}/education/enrollments/{enrollment_id}."""


class TestGetEnrollment:
    """Verify single enrollment retrieval."""

    def test_returns_enrollment_by_id(self, client, company, course):
        """Fetch an enrollment by its ID."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        payload = {"course_id": course["id"], "legal_accepted": True}
        created = client.post(url, json=payload).json()

        response = client.get(f"{url}{created['id']}")

        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_returns_404_for_unknown_id(self, client, company):
        """Unknown enrollment ID should return 404."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"

        response = client.get(f"{url}nonexistent-id")

        assert response.status_code == 404
