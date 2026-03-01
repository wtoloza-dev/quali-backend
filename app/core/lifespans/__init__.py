"""FastAPI lifespan event handlers (startup and shutdown) for the Quali API."""

from .lifespan import lifespan


__all__ = ["lifespan"]
