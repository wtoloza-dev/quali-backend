"""SQL client port — interface contract for database adapters."""

from .async_sql_client_port import AsyncSQLClientPort


__all__ = ["AsyncSQLClientPort"]
