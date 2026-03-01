"""E2e tests for PATCH /api/v1/companies/{company_id}/certificates/{cert_id}/revoke."""

ISSUE_PAYLOAD = {
    "recipient_id": "01ARZ3NDEKTSV4RRFFQ69G5FAR",
    "title": "Python Fundamentals",
}
REVOKE_BODY = {"reason": "Violation of terms."}


class TestRevokeCertificate:
    """Tests for revoking a certificate."""

    def _revoke_url(self, company_id: str, cert_id: str) -> str:
        """Build the revoke URL for a given company and certificate."""
        return f"/api/v1/companies/{company_id}/certificates/{cert_id}/revoke"

    def test_revokes_active_certificate(self, client, company):
        """Should revoke an active certificate and return revocation details."""
        company_id = company["id"]
        issue_url = f"/api/v1/companies/{company_id}/certificates/"

        cert_id = client.post(issue_url, json=ISSUE_PAYLOAD).json()["id"]

        response = client.patch(
            self._revoke_url(company_id, cert_id), json=REVOKE_BODY
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "revoked"
        assert data["revoked_reason"] == REVOKE_BODY["reason"]
        assert data["revoked_at"] is not None

    def test_returns_409_when_already_revoked(self, client, company):
        """Should return 409 when trying to revoke an already revoked certificate."""
        company_id = company["id"]
        issue_url = f"/api/v1/companies/{company_id}/certificates/"

        cert_id = client.post(issue_url, json=ISSUE_PAYLOAD).json()["id"]
        client.patch(self._revoke_url(company_id, cert_id), json=REVOKE_BODY)

        response = client.patch(
            self._revoke_url(company_id, cert_id), json=REVOKE_BODY
        )

        assert response.status_code == 409

    def test_returns_404_for_unknown_certificate(self, client, company):
        """Should return 404 when the certificate does not exist."""
        company_id = company["id"]

        response = client.patch(
            self._revoke_url(company_id, "nonexistent"), json=REVOKE_BODY
        )

        assert response.status_code == 404

    def test_returns_422_when_reason_missing(self, client, company):
        """Should return 422 when the revoke reason is not provided."""
        company_id = company["id"]
        issue_url = f"/api/v1/companies/{company_id}/certificates/"

        cert_id = client.post(issue_url, json=ISSUE_PAYLOAD).json()["id"]

        response = client.patch(
            self._revoke_url(company_id, cert_id), json={}
        )

        assert response.status_code == 422
