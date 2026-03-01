"""Shared pagination schemas for list endpoints."""

import math

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Query parameters for paginated list requests.

    Attributes:
        page: The 1-based page number to retrieve.
        page_size: The number of items per page (max 100).
    """

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        """Return the SQL offset corresponding to the requested page.

        Returns:
            The number of rows to skip before the current page.
        """
        return (self.page - 1) * self.page_size

    def pages(self, total: int) -> int:
        """Return the total number of pages for a given record count.

        Args:
            total: The total number of records across all pages.

        Returns:
            The number of pages required to display all records.
        """
        return math.ceil(total / self.page_size) if self.page_size else 0


class PaginatedResponse[T](BaseModel):
    """Generic paginated response envelope.

    Attributes:
        items: The list of items on the current page.
        total: The total number of records across all pages.
        page: The current 1-based page number.
        page_size: The number of items per page.
        pages: The total number of pages.
    """

    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int
