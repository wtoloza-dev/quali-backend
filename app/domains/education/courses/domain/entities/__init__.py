"""Courses subdomain domain entities."""

from .course_access_entity import CourseAccessData, CourseAccessEntity
from .course_entity import CourseData, CourseEntity
from .lesson_entity import ContentBlock, LessonData, LessonEntity
from .module_entity import ModuleData, ModuleEntity


__all__ = [
    "CourseData",
    "CourseEntity",
    "ModuleData",
    "ModuleEntity",
    "ContentBlock",
    "LessonData",
    "LessonEntity",
    "CourseAccessData",
    "CourseAccessEntity",
]
