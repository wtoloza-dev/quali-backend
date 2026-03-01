"""Shared domain exceptions used across all bounded contexts."""

from ._domain_exception import DomainException
from .conflict_exception import ConflictException
from .forbidden_exception import ForbiddenException
from .insufficient_permissions_exception import InsufficientPermissionsException
from .not_found_exception import NotFoundException
from .unauthorized_exception import UnauthorizedException
from .unprocessable_exception import UnprocessableException


__all__ = [
    "DomainException",
    "NotFoundException",
    "ConflictException",
    "UnauthorizedException",
    "ForbiddenException",
    "InsufficientPermissionsException",
    "UnprocessableException",
]
