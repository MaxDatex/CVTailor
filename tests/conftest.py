from uuid import uuid4

import pytest

from src.core.models.input_cv_fields import (
    CVBody,
    CVHeader,
    Location,
    ProfessionalSummary,
)


@pytest.fixture(scope="session")
def sample_cv_body_data():
    """Provides a sample CVBody object for tests."""
    location_dmytro = Location(city="Lviv", region="Lviv Region", countryCode="UA")
    header_dmytro = CVHeader(
        full_name="Dmytro Kovalenko",
        professional_title="Data Scientist",
        email_address="dmytro.kovalenko@email.com",
        phone_number="+380679876543",
        github_url="http://github.com/dmytrodata",
        linkedin_url="http://linkedin.com/in/dmytrokovalenko",
        location=location_dmytro,
    )
    summary_dmytro = ProfessionalSummary(
        summary="Analytical Data Scientist with experience.",
        highlights=["Skilled in Python."],
    )
    return CVBody(
        header=header_dmytro,
        professional_summary=summary_dmytro,
    )


# @pytest.fixture
# def mock_settings_env(monkeypatch):
#     """Fixture to mock environment variables for settings, if needed."""
#     monkeypatch.setenv("GOOGLE_API_KEY", "test_fixture_api_key")


@pytest.fixture(scope="session")
def valid_summary_data():
    """Provides valid summary data for tests."""
    yield "This is a valid summary with more than fifty characters to satisfy the validation."


@pytest.fixture(scope="session")
def valid_highlights_data():
    """Provides valid highlights data for tests."""
    yield ["Valid highlight 1", "Valid highlight 2"]


@pytest.fixture(scope="session")
def valid_id():
    """Provides valid ID data for tests."""
    yield uuid4().hex
