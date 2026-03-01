"""E2e tests for DELETE /api/v1/companies/{company_id}/education/enrollments/{enrollment_id}."""


class TestUnenroll:
    """Verify enrollment deletion (unenroll)."""

    def test_deletes_enrollment_successfully(self, client, company, course):
        """Deleting an enrollment should return 204."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        payload = {"course_id": course["id"], "legal_accepted": True}
        created = client.post(url, json=payload).json()

        response = client.delete(f"{url}{created['id']}")

        assert response.status_code == 204

    def test_enrollment_no_longer_retrievable_after_delete(
        self, client, company, course
    ):
        """A deleted enrollment should not be retrievable."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        payload = {"course_id": course["id"], "legal_accepted": True}
        created = client.post(url, json=payload).json()
        client.delete(f"{url}{created['id']}")

        response = client.get(f"{url}{created['id']}")

        assert response.status_code == 404

    def test_returns_404_for_unknown_enrollment(self, client, company):
        """Deleting an unknown enrollment should return 404."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"

        response = client.delete(f"{url}nonexistent-id")

        assert response.status_code == 404
