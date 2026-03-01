"""E2e tests for GET /api/v1/companies/{company_id}/certificates/{certificate_id}."""

ISSUE_PAYLOAD = {
    "recipient_id": "01ARZ3NDEKTSV4RRFFQ69G5FAR",
    "title": "Python Fundamentals",
}


class TestGetCertificate:
    """Tests for retrieving a certificate by ID."""

    def test_returns_certificate_by_id(self, client, company):
        """Should return the certificate when fetched by its ID."""
        company_id = company["id"]
        issue_url = f"/api/v1/companies/{company_id}/certificates/"

        cert_id = client.post(issue_url, json=ISSUE_PAYLOAD).json()["id"]

        response = client.get(
            f"/api/v1/companies/{company_id}/certificates/{cert_id}"
        )

        assert response.status_code == 200
        assert response.json()["id"] == cert_id

    def test_returns_404_for_unknown_id(self, client, company):
        """Should return 404 when the certificate ID does not exist."""
        company_id = company["id"]

        response = client.get(
            f"/api/v1/companies/{company_id}/certificates/nonexistent"
        )

        assert response.status_code == 404

    def test_returns_404_for_wrong_company(self, client, company):
        """Should return 404 when querying with a different company ID."""
        company_id = company["id"]
        issue_url = f"/api/v1/companies/{company_id}/certificates/"

        cert_id = client.post(issue_url, json=ISSUE_PAYLOAD).json()["id"]

        # Create a second company to test tenant isolation
        other_company = client.post(
            "/api/v1/companies/",
            json={
                "name": "Other Company",
                "slug": "other-company",
                "company_type": "organization",
                "email": "other@company.com",
                "country": "CO",
            },
        )
        assert other_company.status_code == 201
        other_company_id = other_company.json()["id"]

        # Same cert ID but different company_id — tenant isolation
        response = client.get(
            f"/api/v1/companies/{other_company_id}/certificates/{cert_id}"
        )

        assert response.status_code == 404
