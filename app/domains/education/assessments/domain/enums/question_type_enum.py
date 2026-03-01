"""Question type enum."""

from enum import StrEnum


class QuestionType(StrEnum):
    """Supported question types for assessments.

    Attributes:
        MULTIPLE_CHOICE_SINGLE: One correct answer among options.
        MULTIPLE_CHOICE_MULTI: One or more correct answers.
        TRUE_FALSE: Binary true/false question.
        WORD_SEARCH: Find hidden words in a letter grid.
        CROSSWORD: Fill answers from clues in a crossword grid.
    """

    MULTIPLE_CHOICE_SINGLE = "multiple_choice_single"
    MULTIPLE_CHOICE_MULTI = "multiple_choice_multi"
    TRUE_FALSE = "true_false"
    WORD_SEARCH = "word_search"
    CROSSWORD = "crossword"
