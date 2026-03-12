"""Type-specific configuration schemas for assessment questions.

Uses Pydantic discriminated unions so the correct schema is selected
automatically based on the ``type`` discriminator field.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


# ── Multiple-choice / True-false ──────────────────────────────────────


class MCOption(BaseModel):
    """A single answer option within a MC/TF question."""

    text: str
    is_correct: bool


class MultipleChoiceConfig(BaseModel):
    """Config for MC / TF questions."""

    type: Literal["multiple_choice"] = "multiple_choice"
    options: list[MCOption] = []


# ── Word Search ────────────────────────────────────────────────────────


class WordPosition(BaseModel):
    """Position of a word within a word-search grid."""

    word: str
    row: int
    col: int
    direction: Literal["horizontal", "vertical", "diagonal_down", "diagonal_up"]


class WordSearchConfig(BaseModel):
    """Config for word-search questions."""

    type: Literal["word_search"] = "word_search"
    words: list[str]
    grid_size: int
    grid: list[list[str]]
    word_positions: list[WordPosition]


# ── Crossword ──────────────────────────────────────────────────────────


class CrosswordClue(BaseModel):
    """A single clue entry in a crossword puzzle question."""

    number: int
    direction: Literal["across", "down"]
    clue: str
    answer: str
    row: int
    col: int


class CrosswordConfig(BaseModel):
    """Config for crossword questions."""

    type: Literal["crossword"] = "crossword"
    clues: list[CrosswordClue]
    grid_rows: int
    grid_cols: int


# ── Sorting ────────────────────────────────────────────────────────────


class SortingConfig(BaseModel):
    """Config for sorting/ordering questions.

    Items are stored in correct order — index position IS the answer.
    Frontend shuffles for display, student reorders.
    """

    type: Literal["sorting"] = "sorting"
    items: list[str]


# ── Classification ────────────────────────────────────────────────────


class ClassificationCategory(BaseModel):
    """A single category bucket."""

    label: str


class ClassificationItem(BaseModel):
    """An item to classify."""

    text: str
    correct_category: int


class ClassificationConfig(BaseModel):
    """Config for classification/categorization questions."""

    type: Literal["classification"] = "classification"
    categories: list[ClassificationCategory]
    items: list[ClassificationItem]


# ── Matching ──────────────────────────────────────────────────────────


class MatchingPair(BaseModel):
    """A pair of items to match."""

    left: str
    right: str


class MatchingConfig(BaseModel):
    """Config for matching/pairing questions."""

    type: Literal["matching"] = "matching"
    pairs: list[MatchingPair]


# ── Discriminated union ────────────────────────────────────────────────

QuestionConfig = Annotated[
    MultipleChoiceConfig | WordSearchConfig | CrosswordConfig | SortingConfig | ClassificationConfig | MatchingConfig,
    Field(discriminator="type"),
]
