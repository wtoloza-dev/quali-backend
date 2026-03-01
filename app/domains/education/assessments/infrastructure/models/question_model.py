"""Assessment question ORM model."""

import sqlalchemy as sa
from sqlmodel import Field

from app.shared.models.audit_model import AuditModel

from ...domain.enums import QuestionType


class QuestionModel(AuditModel, table=True):
    """SQLModel ORM model for the assessment_questions table."""

    __tablename__ = "assessment_questions"

    course_id: str = Field(nullable=False, index=True)
    module_id: str | None = Field(default=None, nullable=True, index=True)
    text: str = Field(nullable=False)
    question_type: QuestionType = Field(sa_type=sa.String(), nullable=False)
    config: dict = Field(sa_type=sa.JSON, nullable=False, default_factory=dict)
    randomize: bool = Field(default=True, nullable=False)
    order: int = Field(default=0, nullable=False)
