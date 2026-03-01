"""E2e tests for GET /api/v1/companies/{company_id}/certificates/."""

ISSUE_PAYLOAD = {
    "recipient_id": "01ARZ3NDEKTSV4RRFFQ69G5FAR",
    "title": "Python Fundamentals",
}


class TestListCertificates:
    """Tests for listing certificates."""

    def test_returns_empty_list_when_no_certificates(self, client, company):
        """Should return an empty paginated list when no certificates exist."""
        url = f"/api/v1/companies/{company['id']}/certificates/"

        response = client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_returns_issued_certificates(self, client, company):
        """Should return all issued certificates in the list."""
        url = f"/api/v1/companies/{company['id']}/certificates/"

        client.post(url, json=ISSUE_PAYLOAD)
        client.post(url, json={**ISSUE_PAYLOAD, "title": "Django Advanced"})

        response = client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_pagination_page_size(self, client, company):
        """Should respect page_size parameter for pagination."""
        url = f"/api/v1/companies/{company['id']}/certificates/"

        for i in range(5):
            client.post(url, json={**ISSUE_PAYLOAD, "title": f"Course {i}"})

        response = client.get(url, params={"page": 1, "page_size": 2})

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
