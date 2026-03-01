"""E2e tests for DELETE /api/v1/companies/{company_id}/education/courses/{course_id}/questions/{question_id}."""


def _question_payload(course_id: str) -> dict:
    """Build a valid true/false question payload."""
    return {
        "course_id": course_id,
        "text": "Question to delete",
        "question_type": "true_false",
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "True", "is_correct": True},
                {"text": "False", "is_correct": False},
            ],
        },
    }


class TestDeleteQuestion:
    """Verify assessment question deletion."""

    def test_deletes_question_successfully(self, client, company, course):
        """Deleting a question should return 204."""
        url = f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"
        created = client.post(url, json=_question_payload(course["id"])).json()

        response = client.delete(f"{url}{created['id']}")

        assert response.status_code == 204

    def test_question_not_in_list_after_delete(self, client, company, course):
        """A deleted question should not appear in the list."""
        url = f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"
        created = client.post(url, json=_question_payload(course["id"])).json()
        client.delete(f"{url}{created['id']}")

        response = client.get(url)

        assert response.json() == []

    def test_returns_404_for_unknown_question(self, client, company, course):
        """Deleting an unknown question should return 404."""
        url = f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"

        response = client.delete(f"{url}nonexistent-id")

        assert response.status_code == 404
