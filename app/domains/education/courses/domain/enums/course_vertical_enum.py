"""Course vertical enum."""

from enum import StrEnum


class CourseVertical(StrEnum):
    """Regulatory vertical a course belongs to.

    Attributes:
        SST: Occupational safety and health (SG-SST, Res. 0312).
        FOOD_QUALITY: Food quality and handling (BPM/HACCP, Res. 2674).
        GENERAL: Cross-cutting content not tied to a specific vertical.
    """

    SST = "sst"
    FOOD_QUALITY = "food_quality"
    GENERAL = "general"
