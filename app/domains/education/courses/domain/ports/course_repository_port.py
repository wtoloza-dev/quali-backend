"""Course repository port."""

from typing import Protocol

from ..entities import CourseEntity


class CourseRepositoryPort(Protocol):
    """Interface for the course repository.

    Defined in the domain layer so use cases depend on this abstraction,
    not on the concrete SQLModel implementation.
    """

    async def save(self, entity: CourseEntity) -> CourseEntity:
        """Persist a new course and return the saved state.

        Args:
            entity: The course entity to persist.

        Returns:
            CourseEntity: The persisted entity with DB-generated fields.
        """
        ...

    async def get_by_id(self, course_id: str) -> CourseEntity | None:
        """Retrieve a course by ULID. Returns None if not found.

        Args:
            course_id: The ULID of the course.

        Returns:
            CourseEntity if found, None otherwise.
        """
        ...

    async def get_by_id_and_company(
        self, course_id: str, company_id: str
    ) -> CourseEntity | None:
        """Retrieve a course only if it belongs to the given company.

        Used to enforce tenant isolation on write operations. Public courses
        owned by other companies are excluded — editing is owner-only.

        Args:
            course_id: The ULID of the course.
            company_id: The company that must own the course.

        Returns:
            CourseEntity if found and owned by company, None otherwise.
        """
        ...

    async def update(self, entity: CourseEntity) -> CourseEntity:
        """Persist changes to an existing course entity.

        Args:
            entity: The course entity with updated fields.

        Returns:
            CourseEntity: The updated entity after persistence.
        """
        ...

    async def delete(self, course_id: str, deleted_by: str) -> None:
        """Hard-delete a course and archive a tombstone snapshot.

        Args:
            course_id: The ULID of the course to delete.
            deleted_by: ULID of the user performing the deletion.
        """
        ...

    async def list(
        self,
        page: int,
        page_size: int,
        company_id: str,
    ) -> tuple[list[CourseEntity], int]:
        """Return paginated courses visible to a company.

        Includes courses owned by the company AND all public courses.

        Args:
            page: 1-based page number.
            page_size: Number of items per page.
            company_id: The requesting company's ID.

        Returns:
            Tuple of (list of CourseEntity, total count).
        """
        ...
