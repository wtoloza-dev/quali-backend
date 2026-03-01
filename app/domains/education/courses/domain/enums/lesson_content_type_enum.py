"""Lesson content block type enum."""

from enum import StrEnum


class LessonContentType(StrEnum):
    """Discriminator for lesson content blocks.

    Attributes:
        TEXT: Rich text / HTML body.
        VIDEO: Embedded video from YouTube, Vimeo, or hosted storage.
        FILE: Downloadable file attachment (PDF, PPT, etc.).
    """

    TEXT = "text"
    VIDEO = "video"
    FILE = "file"
