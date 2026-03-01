"""Generate access codes use case dependency factory."""

from typing import Annotated

from fastapi import Depends

from ...application.use_cases import GenerateAccessCodesUseCase
from .build_access_code_repository_dependency import AccessCodeRepositoryDependency


def build_generate_access_codes_use_case(
    repository: AccessCodeRepositoryDependency,
) -> GenerateAccessCodesUseCase:
    """Build a GenerateAccessCodesUseCase with an injected repository.

    Args:
        repository: Access code repository injected by FastAPI.

    Returns:
        GenerateAccessCodesUseCase: Use case instance ready for execution.
    """
    return GenerateAccessCodesUseCase(repository=repository)


GenerateAccessCodesUseCaseDependency = Annotated[
    GenerateAccessCodesUseCase,
    Depends(build_generate_access_codes_use_case),
]
