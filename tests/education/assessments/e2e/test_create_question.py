"""E2e tests for POST /api/v1/companies/{company_id}/education/courses/{course_id}/questions/."""


def _question_payload(course_id: str) -> dict:
    """Build a valid question payload for the given course."""
    return {
        "course_id": course_id,
        "text": "What is 2 + 2?",
        "question_type": "multiple_choice_single",
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "3", "is_correct": False},
                {"text": "4", "is_correct": True},
            ],
        },
    }


class TestCreateQuestion:
    """Verify assessment question creation."""

    def test_returns_201_with_question(self, client, company, course):
        """Create a question and verify the response payload."""
        url = f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"
        payload = _question_payload(course["id"])

        response = client.post(url, json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["text"] == "What is 2 + 2?"
        assert data["course_id"] == course["id"]
        assert data["question_type"] == "multiple_choice_single"
        assert len(data["config"]["options"]) == 2
        assert "id" in data

    def test_options_preserve_is_correct_flag(self, client, company, course):
        """The is_correct flag on options should be preserved."""
        url = f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"
        payload = _question_payload(course["id"])

        response = client.post(url, json=payload)

        options = response.json()["config"]["options"]
        assert options[0]["is_correct"] is False
        assert options[1]["is_correct"] is True

    def test_missing_required_field_returns_422(self, client, company, course):
        """Missing text field should return 422."""
        url = f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"
        payload = _question_payload(course["id"])
        del payload["text"]

        response = client.post(url, json=payload)

        assert response.status_code == 422
