"""Enrollment access type enum."""

from __future__ import annotations

from enum import StrEnum


class AccessType(StrEnum):
    """Level of content access for an enrollment.

    Attributes:
        PREVIEW: User can only view preview lessons.
        FULL: User has full access to all course content.
    """

    PREVIEW = "preview"
    FULL = "full"
