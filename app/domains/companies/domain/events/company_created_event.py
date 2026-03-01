"""Company created domain event."""

from pydantic import BaseModel


class CompanyCreatedEvent(BaseModel):
    """Emitted when a new company is successfully registered.

    Consumed by domains that react to company creation, such as
    provisioning default settings or sending welcome notifications.

    Attributes:
        company_id: ID of the newly created company.
        created_by: ID of the user who created the company.
    """

    company_id: str
    created_by: str
