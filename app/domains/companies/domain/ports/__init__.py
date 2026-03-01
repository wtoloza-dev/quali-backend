"""Domain ports (interfaces) for the Companies domain."""

from .company_member_repository_port import CompanyMemberRepositoryPort
from .company_repository_port import CompanyRepositoryPort


__all__ = ["CompanyRepositoryPort", "CompanyMemberRepositoryPort"]
