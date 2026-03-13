"""E2e tests for POST /api/v1/companies/{company_id}/education/enrollments/."""


class TestEnrollUser:
    """Verify enrollment creation via the enrollments endpoint."""

    def test_returns_201_with_enrollment(self, client, company, course):
        """Create an enrollment and verify the response payload."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        payload = {"course_id": course["id"], "legal_accepted": True}

        response = client.post(url, json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["course_id"] == course["id"]
        assert data["status"] == "not_started"
        assert data["access_type"] == "preview"
        assert data["start_date"] is None
        assert data["end_date"] is None
        assert "id" in data
        assert "enrolled_at" in data

    def test_is_mandatory_defaults_to_false(self, client, company, course):
        """Enrollment is_mandatory should default to False."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        payload = {"course_id": course["id"], "legal_accepted": True}

        response = client.post(url, json=payload)

        assert response.json()["is_mandatory"] is False

    def test_is_mandatory_can_be_true(self, client, company, course):
        """Enrollment is_mandatory can be set to True explicitly."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        payload = {
            "course_id": course["id"],
            "legal_accepted": True,
            "is_mandatory": True,
        }

        response = client.post(url, json=payload)

        assert response.status_code == 201
        assert response.json()["is_mandatory"] is True

    def test_missing_required_field_returns_422(self, client, company):
        """Missing course_id should return 422."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"

        response = client.post(url, json={"legal_accepted": True})

        assert response.status_code == 422

    def test_completed_at_is_null_on_creation(self, client, company, course):
        """A fresh enrollment must have completed_at as None."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        payload = {"course_id": course["id"], "legal_accepted": True}

        response = client.post(url, json=payload)

        assert response.json()["completed_at"] is None
