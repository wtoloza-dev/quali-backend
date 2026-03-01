"""Training plan not found exception."""

from app.shared.exceptions import NotFoundException


class TrainingPlanNotFoundException(NotFoundException):
    """Raised when a training plan cannot be found by the given ID."""

    def __init__(self, plan_id: str) -> None:
        """Initialise with the missing plan ID.

        Args:
            plan_id: The ULID that was not found.
        """
        super().__init__(
            message=f"Training plan '{plan_id}' not found.",
            context={"plan_id": plan_id},
            error_code="TRAINING_PLAN_NOT_FOUND",
        )
