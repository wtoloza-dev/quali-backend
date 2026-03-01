"""E2e tests for GET /api/v1/companies/{company_id}/education/enrollments/{enrollment_id}/attempts/."""


def _question_payload(course_id: str) -> dict:
    """Build a valid true/false question payload."""
    return {
        "course_id": course_id,
        "text": "True or false?",
        "question_type": "true_false",
        "config": {
            "type": "multiple_choice",
            "options": [
                {"text": "True", "is_correct": True},
                {"text": "False", "is_correct": False},
            ],
        },
    }


class TestListAttempts:
    """Verify assessment attempt listing."""

    def test_returns_empty_list(self, client, company, course, enrollment):
        """No attempts should return an empty list."""
        attempts_url = (
            f"/api/v1/companies/{company['id']}/education/"
            f"enrollments/{enrollment['id']}/attempts/"
        )

        response = client.get(attempts_url)

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_submitted_attempt(self, client, company, course, enrollment):
        """A submitted attempt should appear in the list."""
        questions_url = (
            f"/api/v1/companies/{company['id']}/education/"
            f"courses/{course['id']}/questions/"
        )
        attempts_url = (
            f"/api/v1/companies/{company['id']}/education/"
            f"enrollments/{enrollment['id']}/attempts/"
        )

        question = client.post(
            questions_url, json=_question_payload(course["id"])
        ).json()
        client.post(
            attempts_url,
            json={
                "enrollment_id": enrollment["id"],
                "answers": [
                    {"question_id": question["id"], "selected_indices": [0]},
                ],
            },
        )

        response = client.get(attempts_url)

        assert response.status_code == 200
        assert len(response.json()) == 1
