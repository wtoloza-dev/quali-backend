"""Training plan item not found exception."""

from app.shared.exceptions import NotFoundException


class TrainingPlanItemNotFoundException(NotFoundException):
    """Raised when a training plan item cannot be found by the given ID."""

    def __init__(self, item_id: str) -> None:
        """Initialise with the missing item ID.

        Args:
            item_id: The ULID that was not found.
        """
        super().__init__(
            message=f"Training plan item '{item_id}' not found.",
            context={"item_id": item_id},
            error_code="TRAINING_PLAN_ITEM_NOT_FOUND",
        )
