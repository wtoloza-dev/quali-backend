"""Course not found exception."""


class CourseNotFoundException(Exception):
    """Raised when a course cannot be found by the given identifier.

    Attributes:
        course_id: The identifier that produced no result.
    """

    def __init__(self, course_id: str) -> None:
        """Initialise the exception with the missing course ID.

        Args:
            course_id: The ULID that was not found.
        """
        self.course_id = course_id
        super().__init__(f"Course '{course_id}' not found.")
