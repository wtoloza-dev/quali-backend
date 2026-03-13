"""Assessment attempt ORM model."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlmodel import Field

from app.shared.models.audit_model import AuditModel


class AttemptModel(AuditModel, table=True):
    """SQLModel ORM model for the assessment_attempts table.

    Attributes:
        __tablename__: Database table name.
        enrollment_id: ULID of the parent enrollment.
        score: Percentage score (0–100).
        passed: Whether the score met the passing threshold.
        attempt_number: Sequential attempt number (1-based).
        answers: JSON snapshot of submitted answers.
        taken_at: Timestamp when the attempt was submitted.
    """

    __tablename__ = "assessment_attempts"

    enrollment_id: str = Field(nullable=False, index=True)
    module_id: str | None = Field(default=None, nullable=True, index=True)
    score: int = Field(nullable=False)
    passed: bool = Field(nullable=False)
    attempt_number: int = Field(nullable=False)
    answers: list = Field(sa_type=sa.JSON, nullable=False, default_factory=list)
    correct_question_ids: list = Field(
        sa_type=sa.JSON, nullable=False, default_factory=list
    )
    taken_at: datetime = Field(
        nullable=False,
        sa_type=DateTime(timezone=True),
    )
