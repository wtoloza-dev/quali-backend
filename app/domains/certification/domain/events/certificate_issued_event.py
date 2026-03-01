"""Certificate issued domain event."""

from pydantic import BaseModel


class CertificateIssuedEvent(BaseModel):
    """Emitted when a certificate is successfully issued to a user.

    Consumed by domains that react to certificate issuance, such as
    sending notifications or updating training compliance records.

    Attributes:
        certificate_id: ID of the newly issued certificate.
        recipient_id: User who received the certificate.
        company_id: Tenant that issued the certificate.
        template_id: Certificate template used, if any.
    """

    pass
