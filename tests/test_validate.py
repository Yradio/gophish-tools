#!/usr/bin/env pytest -vs
"""Tests for Validation functions."""

# Third-Party Libraries
import pytest

# cisagov Libraries
from util.validate import (
    FormatError,
    validate_assessment_id,
    validate_domain,
    validate_email,
)


@pytest.mark.parametrize(
    "email", ["name.last@domain.test", "name.last+phish@domain.test"]
)
def test_validate_email_valid(email):
    """Test a valid email address."""
    assert validate_email(email)


@pytest.mark.parametrize("email", ["@domain.test", "phish@test"])
def test_validate_email_invalid(email):
    """Test an invalid email address."""
    with pytest.raises(FormatError):
        validate_email(email)


@pytest.mark.parametrize("email", ["name.last@domain.test"])
@pytest.mark.parametrize("domain", ["domain.test"])
def test_validate_domain_valid(email, domain):
    """Test a valid domain."""
    assert validate_domain(email, domain)


@pytest.mark.parametrize("email", ["name.last@domain.test"])
@pytest.mark.parametrize("domain", ["test.test"])
def test_validate_domain_invalid(email, domain):
    """Test an invalid domain."""
    assert not validate_domain(email, domain)


@pytest.mark.parametrize("assessment_id", ["RV1234"])
def test_validate_assessment_id_valid(assessment_id):
    """Test a valid assessment_id."""
    assert validate_assessment_id(assessment_id)


@pytest.mark.parametrize("assessment_id", ["RV...."])
def test_validate_assessment_id_invalid(assessment_id):
    """Test an invalid assessment_id."""
    assert not validate_assessment_id(assessment_id)
