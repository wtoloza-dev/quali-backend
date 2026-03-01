"""Cross-domain contract ports, result types, and adapters.

Re-exports every contract port, DTO, and FastAPI dependency so that any
domain can import from a single location.

Usage:
    from app.shared.contracts import GetUserByIdPort, GetUserByIdDependency
"""

from .get_company_by_id.get_company_by_id_adapter import (
    GetCompanyByIdAdapter,
    GetCompanyByIdDependency,
)
from .get_company_by_id.get_company_by_id_port import (
    CompanyContractResult,
    GetCompanyByIdPort,
)
from .get_company_member.get_company_member_adapter import (
    GetCompanyMemberAdapter,
    GetCompanyMemberDependency,
)
from .get_company_member.get_company_member_port import (
    CompanyMemberContractResult,
    GetCompanyMemberPort,
)
from .get_user_by_id.get_user_by_id_adapter import (
    GetUserByIdAdapter,
    GetUserByIdDependency,
)
from .get_user_by_id.get_user_by_id_port import GetUserByIdPort, UserContractResult
from .list_certificates_by_recipient.list_certificates_by_recipient_adapter import (
    ListCertificatesByRecipientAdapter,
    ListCertificatesByRecipientDependency,
)
from .list_certificates_by_recipient.list_certificates_by_recipient_port import (
    CertificateContractResult,
    CertificateListContractResult,
    ListCertificatesByRecipientPort,
)
from .save_legal_acceptance.save_legal_acceptance_adapter import (
    SaveLegalAcceptanceAdapter,
    SaveLegalAcceptanceDependency,
)
from .save_legal_acceptance.save_legal_acceptance_port import (
    LegalAcceptanceContractInput,
    SaveLegalAcceptancePort,
)


__all__ = [
    "GetUserByIdPort",
    "UserContractResult",
    "GetUserByIdAdapter",
    "GetUserByIdDependency",
    "GetCompanyByIdPort",
    "CompanyContractResult",
    "GetCompanyByIdAdapter",
    "GetCompanyByIdDependency",
    "GetCompanyMemberPort",
    "CompanyMemberContractResult",
    "GetCompanyMemberAdapter",
    "GetCompanyMemberDependency",
    "CertificateContractResult",
    "CertificateListContractResult",
    "ListCertificatesByRecipientAdapter",
    "ListCertificatesByRecipientDependency",
    "ListCertificatesByRecipientPort",
    "SaveLegalAcceptancePort",
    "LegalAcceptanceContractInput",
    "SaveLegalAcceptanceAdapter",
    "SaveLegalAcceptanceDependency",
]
