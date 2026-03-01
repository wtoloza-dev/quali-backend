"""E2e tests for POST /api/v1/companies/{company_id}/certificates/."""

VALID_PAYLOAD = {
    "recipient_id": "01ARZ3NDEKTSV4RRFFQ69G5FAR",
    "title": "Python Fundamentals",
    "description": "Completed the Python Fundamentals course.",
}


class TestIssueCertificate:
    """Tests for issuing a certificate."""

    def test_returns_201_with_certificate(self, client, company):
        """Should create a certificate and return 201."""
        company_id = company["id"]
        url = f"/api/v1/companies/{company_id}/certificates/"

        response = client.post(url, json=VALID_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Python Fundamentals"
        assert data["company_id"] == company_id
        assert data["recipient_id"] == VALID_PAYLOAD["recipient_id"]
        assert data["status"] == "active"
        assert "id" in data
        assert "token" in data

    def test_token_is_auto_generated(self, client, company):
        """Should generate unique tokens for each certificate."""
        url = f"/api/v1/companies/{company['id']}/certificates/"

        r1 = client.post(url, json=VALID_PAYLOAD)
        r2 = client.post(
            url,
            json={**VALID_PAYLOAD, "recipient_id": "01ARZ3NDEKTSV4RRFFQ69G5FAX"},
        )

        assert r1.json()["token"] != r2.json()["token"]

    def test_accepts_optional_fields(self, client, company):
        """Should accept and persist optional fields like expires_at."""
        url = f"/api/v1/companies/{company['id']}/certificates/"
        payload = {
            **VALID_PAYLOAD,
            "expires_at": "2030-01-01T00:00:00Z",
        }

        response = client.post(url, json=payload)

        assert response.status_code == 201
        assert response.json()["expires_at"] is not None

    def test_missing_required_field_returns_422(self, client, company):
        """Should return 422 when a required field is missing."""
        url = f"/api/v1/companies/{company['id']}/certificates/"
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "title"}

        response = client.post(url, json=payload)

        assert response.status_code == 422
