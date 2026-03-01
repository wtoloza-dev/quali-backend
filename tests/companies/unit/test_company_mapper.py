"""Unit tests for CompanyMapper."""

from app.domains.companies.domain.enums import CompanyType, TaxType
from app.domains.companies.domain.value_objects import Tax
from app.domains.companies.presentation.mappers.company_mapper import CompanyMapper


class TestToPublicResponse:
    def test_returns_public_fields(self, company_entity):
        result = CompanyMapper.to_public_response(company_entity)

        assert result.id == company_entity.id
        assert result.name == company_entity.name
        assert result.slug == company_entity.slug
        assert result.company_type == company_entity.company_type
        assert result.country == company_entity.country
        assert result.legal_name == company_entity.legal_name
        assert result.logo_url == company_entity.logo_url

    def test_excludes_pii_fields(self, company_entity):
        result = CompanyMapper.to_public_response(company_entity)

        assert not hasattr(result, "email")
        assert not hasattr(result, "tax")

    def test_with_null_optional_fields(self, company_entity):
        entity = company_entity.model_copy(
            update={"legal_name": None, "logo_url": None}
        )
        result = CompanyMapper.to_public_response(entity)

        assert result.legal_name is None
        assert result.logo_url is None


class TestToPrivateResponse:
    def test_returns_all_fields(self, company_entity):
        result = CompanyMapper.to_private_response(company_entity)

        assert result.id == company_entity.id
        assert result.name == company_entity.name
        assert result.slug == company_entity.slug
        assert result.company_type == company_entity.company_type
        assert result.email == company_entity.email
        assert result.country == company_entity.country
        assert result.legal_name == company_entity.legal_name
        assert result.logo_url == company_entity.logo_url

    def test_includes_tax_when_present(self, company_entity):
        result = CompanyMapper.to_private_response(company_entity)

        assert result.tax is not None
        assert result.tax.tax_type == TaxType.NIT
        assert result.tax.tax_id == "900123456"

    def test_tax_is_none_when_not_set(self, company_entity):
        entity = company_entity.model_copy(update={"tax": None})
        result = CompanyMapper.to_private_response(entity)

        assert result.tax is None

    def test_personal_company_with_cc(self, company_entity):
        entity = company_entity.model_copy(
            update={
                "company_type": CompanyType.PERSONAL,
                "tax": Tax(tax_type=TaxType.CC, tax_id="1234567890"),
            }
        )
        result = CompanyMapper.to_private_response(entity)

        assert result.company_type == CompanyType.PERSONAL
        assert result.tax.tax_type == TaxType.CC
