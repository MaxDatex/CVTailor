import pytest

from models.input_cv_fields import (CVBody, CVHeader, Location,
                                    ProfessionalSummary)


@pytest.fixture(
    scope="session"
)  # 'session' scope means it's created once per test session
def sample_cv_body_data():
    """Provides a sample CVBody object for tests."""
    # This can be the same data as in your examples/test_template.py
    # For brevity, I'll create a minimal version here
    location_dmytro = Location(city="Lviv", region="Lviv Region", countryCode="UA")
    header_dmytro = CVHeader(
        full_name="Dmytro Kovalenko",
        professional_title="Data Scientist",
        email_address="dmytro.kovalenko@email.com",
        phone_number="+380679876543",  # Ensure format matches PhoneNumber expectation
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
        # Add other sections as needed for your tests
    )


@pytest.fixture
def mock_settings_env(monkeypatch):
    """Fixture to mock environment variables for settings, if needed."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_fixture_api_key")
