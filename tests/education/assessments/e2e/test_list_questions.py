"""E2e tests for GET /api/v1/companies/{company_id}/education/courses/{course_id}/questions/."""


def _question_payload(course_id: str, text: str = "Question text") -> dict:
    """Build a valid true/false question payload."""
    return {
        "course_id": course_id,
        "text": text,
        "question_type": "true_false",
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "True", "is_correct": True},
                {"text": "False", "is_correct": False},
            ],
        },
    }


class TestListQuestions:
    """Verify assessment question listing."""

    def test_returns_empty_list(self, client, company, course):
        """No questions should return an empty list."""
        url = f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"

        response = client.get(url)

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_created_questions(self, client, company, course):
        """Created questions should appear in the list."""
        url = f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"
        client.post(url, json=_question_payload(course["id"]))
        client.post(url, json=_question_payload(course["id"], "Another question"))

        response = client.get(url)

        assert response.status_code == 200
        assert len(response.json()) == 2
