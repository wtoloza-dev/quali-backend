"""get_company_by_id contract — port, result DTO, and adapter."""

from .get_company_by_id_adapter import GetCompanyByIdAdapter, GetCompanyByIdDependency
from .get_company_by_id_port import CompanyContractResult, GetCompanyByIdPort


__all__ = [
    "GetCompanyByIdPort",
    "CompanyContractResult",
    "GetCompanyByIdAdapter",
    "GetCompanyByIdDependency",
]
