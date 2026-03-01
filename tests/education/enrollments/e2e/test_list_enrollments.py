"""E2e tests for GET /api/v1/companies/{company_id}/education/enrollments/."""


class TestListEnrollments:
    """Verify enrollment listing and pagination."""

    def test_returns_empty_list(self, client, company):
        """No enrollments should return an empty paginated result."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"

        response = client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_returns_created_enrollment(self, client, company, course):
        """Creating an enrollment should make it appear in the list."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"
        client.post(url, json={"course_id": course["id"], "legal_accepted": True})

        response = client.get(url)

        assert response.json()["total"] == 1
        assert len(response.json()["items"]) == 1

    def test_pagination_fields_present(self, client, company):
        """Paginated response must contain standard pagination fields."""
        url = f"/api/v1/companies/{company['id']}/education/enrollments/"

        response = client.get(url)

        data = response.json()
        assert "page" in data
        assert "page_size" in data
        assert "total" in data
        assert "items" in data
