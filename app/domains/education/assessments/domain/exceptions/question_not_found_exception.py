"""Question not found exception."""

from app.shared.exceptions import NotFoundException


class QuestionNotFoundException(NotFoundException):
    """Raised when a question cannot be found by the given ID.

    Args:
        question_id: The ULID that was not found.
    """

    def __init__(self, question_id: str) -> None:
        """Initialise with the missing question ID.

        Args:
            question_id: The ULID that was not found.
        """
        super().__init__(
            message=f"Question '{question_id}' not found.",
            context={"question_id": question_id},
            error_code="QUESTION_NOT_FOUND",
        )
