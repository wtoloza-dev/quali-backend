"""Reorder request schema."""

from pydantic import BaseModel, Field


class ReorderItemSchema(BaseModel):
    """A single item in a reorder request.

    Attributes:
        id: ULID of the item (module or lesson).
        order: New order value (1-based).
    """

    id: str
    order: int = Field(ge=1)


class ReorderRequestSchema(BaseModel):
    """Input schema for reorder endpoints.

    Attributes:
        items: List of items with their new order values.
    """

    items: list[ReorderItemSchema]
