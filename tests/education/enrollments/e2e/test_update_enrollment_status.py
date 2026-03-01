"""E2e tests for PATCH /api/v1/companies/{company_id}/education/enrollments/{enrollment_id}/status."""


class TestUpdateEnrollmentStatus:
    """Verify enrollment status transitions."""

    def _enroll(self, client, company, course):
        """Create an enrollment and return its JSON response."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        payload = {"course_id": course["id"], "legal_accepted": True}
        return client.post(url, json=payload).json()

    def test_updates_status_to_in_progress(self, client, company, course):
        """Transition from not_started to in_progress should succeed."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        created = self._enroll(client, company, course)

        response = client.patch(
            f"{url}{created['id']}/status",
            json={"status": "in_progress"},
        )

        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    def test_sets_completed_at_when_completed(self, client, company, course):
        """Completing an enrollment should set completed_at."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        created = self._enroll(client, company, course)
        client.patch(
            f"{url}{created['id']}/status",
            json={"status": "in_progress"},
        )

        response = client.patch(
            f"{url}{created['id']}/status",
            json={"status": "completed"},
        )

        assert response.status_code == 200
        assert response.json()["completed_at"] is not None

    def test_invalid_transition_returns_422(self, client, company, course):
        """Skipping in_progress (not_started -> completed) should fail."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        created = self._enroll(client, company, course)

        response = client.patch(
            f"{url}{created['id']}/status",
            json={"status": "completed"},
        )

        assert response.status_code == 422

    def test_returns_404_for_unknown_enrollment(self, client, company):
        """Status update for unknown enrollment should return 404."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"

        response = client.patch(
            f"{url}nonexistent/status",
            json={"status": "in_progress"},
        )

        assert response.status_code == 404

    def test_invalid_status_value_returns_422(self, client, company, course):
        """An invalid status value should return 422."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        created = self._enroll(client, company, course)

        response = client.patch(
            f"{url}{created['id']}/status",
            json={"status": "invalid_status"},
        )

        assert response.status_code == 422
