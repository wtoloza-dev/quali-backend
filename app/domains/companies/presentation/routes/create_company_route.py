"""Create company route handler."""

from typing import Annotated

from fastapi import APIRouter, Body, status

from app.shared.auth.dependencies import CurrentUserDependency
from app.shared.auth.role import Role

from ...domain.entities import CompanyData, CompanyMemberData
from ...infrastructure.dependencies import (
    AddCompanyMemberUseCaseDependency,
    CreateCompanyUseCaseDependency,
)
from ..mappers.company_mapper import CompanyMapper
from ..schemas import CompanyPrivateResponseSchema, CreateCompanyRequestSchema


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new company",
    description="Registers a new company and grants the creator OWNER role.",
)
async def handle_create_company_route(
    body: Annotated[CreateCompanyRequestSchema, Body()],
    use_case: CreateCompanyUseCaseDependency,
    add_member_use_case: AddCompanyMemberUseCaseDependency,
    auth: CurrentUserDependency,
) -> CompanyPrivateResponseSchema:
    """Handle POST requests to register a new company.

    Creates the company and immediately adds the creator as an OWNER member
    so they can manage the company without a separate step.

    Args:
        body: Validated company registration request.
        use_case: Injected CreateCompanyUseCase.
        add_member_use_case: Injected AddCompanyMemberUseCase.
        auth: Authenticated user context.

    Returns:
        CompanyPrivateResponseSchema: The newly created company data.
    """
    company = await use_case.execute(
        CompanyData.model_validate(body.model_dump()),
        created_by=auth.user_id,
    )
    await add_member_use_case.execute(
        data=CompanyMemberData(
            company_id=company.id,
            user_id=auth.user_id,
            role=Role.OWNER,
        ),
        created_by=auth.user_id,
    )
    return CompanyMapper.to_private_response(company)
