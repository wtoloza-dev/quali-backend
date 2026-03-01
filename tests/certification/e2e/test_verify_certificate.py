"""E2e tests for GET /api/v1/certificates/verify/{token}."""

ISSUE_PAYLOAD = {
    "recipient_id": "01ARZ3NDEKTSV4RRFFQ69G5FAR",
    "title": "Python Fundamentals",
}


class TestVerifyCertificate:
    """Tests for verifying a certificate by token."""

    def test_returns_certificate_for_valid_token(self, client, company):
        """Should return the certificate when verified with a valid token."""
        issue_url = f"/api/v1/companies/{company['id']}/certificates/"

        issued = client.post(issue_url, json=ISSUE_PAYLOAD).json()
        token = issued["token"]

        response = client.get(f"/api/v1/certificates/verify/{token}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == issued["id"]
        assert data["title"] == "Python Fundamentals"
        assert data["status"] == "active"

    def test_returns_404_for_unknown_token(self, client, company):
        """Should return 404 when the token does not match any certificate."""
        response = client.get("/api/v1/certificates/verify/nonexistent-token")

        assert response.status_code == 404

    def test_verify_response_omits_audit_fields(self, client, company):
        """Should omit sensitive audit fields from the verify response."""
        issue_url = f"/api/v1/companies/{company['id']}/certificates/"

        token = client.post(issue_url, json=ISSUE_PAYLOAD).json()["token"]

        data = client.get(f"/api/v1/certificates/verify/{token}").json()

        assert "created_by" not in data
        assert "updated_by" not in data
        assert "token" not in data
