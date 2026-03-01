"""E2e tests for company member routes."""

BASE_URL = "/api/v1/companies/"

USER_ID_1 = "01ARZ3NDEKTSV4RRFFQ69G5FB1"
USER_ID_2 = "01ARZ3NDEKTSV4RRFFQ69G5FB2"


class TestAddCompanyMember:
    """Tests for adding a member to a company."""

    def test_returns_201_with_member_data(self, client, company):
        """Adding a new member returns 201 with member details."""
        response = client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_1},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["company_id"] == company["id"]
        assert data["user_id"] == USER_ID_1
        assert "id" in data
        assert "created_at" in data

    def test_duplicate_member_returns_409(self, client, company):
        """Adding the same user twice returns 409."""
        client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_1},
        )
        response = client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_1},
        )

        assert response.status_code == 409
        assert response.json()["error_code"] == "COMPANY_MEMBER_ALREADY_EXISTS"

    def test_missing_user_id_returns_422(self, client, company):
        """Omitting user_id in the payload returns 422."""
        response = client.post(f"{BASE_URL}{company['id']}/members", json={})

        assert response.status_code == 422


class TestGetCompanyMembers:
    """Tests for listing company members."""

    def test_returns_owner_for_new_company(self, client, company):
        """A new company has the OWNER as the only member."""
        response = client.get(f"{BASE_URL}{company['id']}/members")

        assert response.status_code == 200
        members = response.json()
        assert len(members) == 1
        assert members[0]["role"] == "owner"

    def test_returns_added_members(self, client, company):
        """Added members appear in the list alongside the OWNER."""
        client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_1},
        )
        client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_2},
        )
        response = client.get(f"{BASE_URL}{company['id']}/members")

        assert response.status_code == 200
        assert len(response.json()) == 3  # OWNER + 2 added

    def test_deleted_members_are_excluded(self, client, company):
        """Removed members no longer appear in the list."""
        client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_1},
        )
        client.delete(f"{BASE_URL}{company['id']}/members/{USER_ID_1}")
        response = client.get(f"{BASE_URL}{company['id']}/members")

        assert response.status_code == 200
        assert len(response.json()) == 1  # only OWNER remains


class TestRemoveCompanyMember:
    """Tests for removing a member from a company."""

    def test_returns_204_on_success(self, client, company):
        """Removing an existing member returns 204."""
        client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_1},
        )
        response = client.delete(f"{BASE_URL}{company['id']}/members/{USER_ID_1}")

        assert response.status_code == 204

    def test_nonexistent_member_returns_404(self, client, company):
        """Removing a user who was never added returns 404."""
        response = client.delete(f"{BASE_URL}{company['id']}/members/{USER_ID_1}")

        assert response.status_code == 404
        assert response.json()["error_code"] == "COMPANY_MEMBER_NOT_FOUND"

    def test_already_removed_returns_404(self, client, company):
        """Removing the same member twice returns 404 on the second call."""
        client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_1},
        )
        client.delete(f"{BASE_URL}{company['id']}/members/{USER_ID_1}")
        response = client.delete(f"{BASE_URL}{company['id']}/members/{USER_ID_1}")

        assert response.status_code == 404
        assert response.json()["error_code"] == "COMPANY_MEMBER_NOT_FOUND"

    def test_same_user_different_companies(self, client, company):
        """Same user can be a member of two different companies."""
        company_2 = client.post(
            BASE_URL,
            json={
                "name": "Second Company",
                "slug": "second-company",
                "company_type": "organization",
                "email": "info@second.com",
                "country": "CO",
            },
        ).json()

        client.post(
            f"{BASE_URL}{company['id']}/members",
            json={"user_id": USER_ID_1},
        )
        client.post(
            f"{BASE_URL}{company_2['id']}/members",
            json={"user_id": USER_ID_1},
        )
        response = client.get(f"{BASE_URL}{company['id']}/members")

        # OWNER + USER_ID_1 for the first company
        assert len(response.json()) == 2
