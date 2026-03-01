"""E2e tests for POST /api/v1/companies/."""

BASE_URL = "/api/v1/companies/"

VALID_PAYLOAD = {
    "name": "Acme Corp",
    "slug": "acme-corp",
    "company_type": "organization",
    "email": "contact@acme.com",
    "country": "CO",
}


class TestCreateCompany:
    """Tests for company creation endpoint."""

    def test_returns_201_with_private_response(self, client):
        """Successful creation returns 201 with all company fields."""
        response = client.post(BASE_URL, json=VALID_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Acme Corp"
        assert data["slug"] == "acme-corp"
        assert data["email"] == "contact@acme.com"
        assert data["country"] == "CO"
        assert data["company_type"] == "organization"
        assert "id" in data

    def test_response_excludes_no_pii(self, client):
        """Private response must include email and tax."""
        response = client.post(BASE_URL, json=VALID_PAYLOAD)

        data = response.json()
        assert "email" in data
        assert "tax" in data

    def test_with_optional_tax(self, client):
        """Tax info is stored when provided."""
        payload = {
            **VALID_PAYLOAD,
            "slug": "acme-tax",
            "tax": {"tax_type": "NIT", "tax_id": "900123456"},
        }
        response = client.post(BASE_URL, json=payload)

        assert response.status_code == 201
        assert response.json()["tax"]["tax_id"] == "900123456"

    def test_duplicate_slug_returns_409(self, client):
        """Creating two companies with the same slug returns 409."""
        client.post(BASE_URL, json=VALID_PAYLOAD)
        response = client.post(BASE_URL, json=VALID_PAYLOAD)

        assert response.status_code == 409
        assert response.json()["error_code"] == "COMPANY_SLUG_TAKEN"

    def test_personal_company_with_cc_tax(self, client):
        """Personal company type accepts CC tax type."""
        payload = {
            **VALID_PAYLOAD,
            "slug": "john-doe",
            "company_type": "personal",
            "tax": {"tax_type": "CC", "tax_id": "1234567890"},
        }
        response = client.post(BASE_URL, json=payload)

        assert response.status_code == 201
        assert response.json()["company_type"] == "personal"
        assert response.json()["tax"]["tax_type"] == "CC"

    def test_missing_required_field_returns_422(self, client):
        """Omitting a required field returns 422."""
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "email"}
        response = client.post(BASE_URL, json=payload)

        assert response.status_code == 422
