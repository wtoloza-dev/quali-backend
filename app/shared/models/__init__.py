"""Shared ORM base models used across all domains."""

from .audit_model import AuditModel
from .entity_tombstone_model import EntityTombstoneModel


__all__ = ["AuditModel", "EntityTombstoneModel"]
