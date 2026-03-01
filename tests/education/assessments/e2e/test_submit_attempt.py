"""E2e tests for POST /api/v1/companies/{company_id}/education/enrollments/{enrollment_id}/attempts/."""


def _question_payload(course_id: str) -> dict:
    """Build a valid multiple-choice question payload."""
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


def _setup(client, company, course, enrollment):
    """Create a question and return URLs + question JSON."""
    questions_url = (
        f"/api/v1/companies/{company['id']}/education/courses/{course['id']}/questions/"
    )
    attempts_url = (
        f"/api/v1/companies/{company['id']}/education/"
        f"enrollments/{enrollment['id']}/attempts/"
    )
    question = client.post(questions_url, json=_question_payload(course["id"])).json()
    return attempts_url, question


class TestSubmitAttempt:
    """Verify assessment attempt submission and scoring."""

    def test_returns_201_with_attempt(self, client, company, course, enrollment):
        """Submitting a correct answer should return 201 with score 100."""
        attempts_url, question = _setup(client, company, course, enrollment)
        payload = {
            "enrollment_id": enrollment["id"],
            "answers": [
                {"question_id": question["id"], "selected_indices": [1]},
            ],
        }

        response = client.post(attempts_url, json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["enrollment_id"] == enrollment["id"]
        assert data["score"] == 100
        assert data["passed"] is True
        assert data["attempt_number"] == 1
        assert "id" in data

    def test_wrong_answer_scores_zero(self, client, company, course, enrollment):
        """Submitting a wrong answer should score zero."""
        attempts_url, question = _setup(client, company, course, enrollment)
        payload = {
            "enrollment_id": enrollment["id"],
            "answers": [
                {"question_id": question["id"], "selected_indices": [0]},
            ],
        }

        response = client.post(attempts_url, json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["score"] == 0
        assert data["passed"] is False

    def test_invalid_answer_entry_returns_422(
        self, client, company, course, enrollment
    ):
        """Answers must be a list, not a string."""
        attempts_url, _ = _setup(client, company, course, enrollment)

        response = client.post(attempts_url, json={"answers": "not-a-list"})

        assert response.status_code == 422
