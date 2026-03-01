"""Lesson not found exception."""


class LessonNotFoundException(Exception):
    """Raised when a course lesson cannot be found by the given identifier.

    Attributes:
        lesson_id: The identifier that produced no result.
    """

    def __init__(self, lesson_id: str) -> None:
        """Initialise the exception with the missing lesson ID.

        Args:
            lesson_id: The ULID that was not found.
        """
        self.lesson_id = lesson_id
        super().__init__(f"Lesson '{lesson_id}' not found.")
