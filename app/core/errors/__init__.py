"""HTTP error handlers and exception mapper for the Quali API."""

from .error_handler import register_error_handlers
from .error_mapper import DomainExceptionMapper


__all__ = [
    "register_error_handlers",
    "DomainExceptionMapper",
]
