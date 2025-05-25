from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from models.input_cv_fields import (
    EducationItem,
    Location,
    ProfessionalSummary,
    StudyType,
    WorkItem,
)


class TestProfessionalSummary:
    def test_valid_summary(self):
        summary_data = {
            "summary": "This is a valid summary with more than fifty characters to satisfy the validation.",
            "highlights": ["Valid highlight one.", "Valid highlight two."],
        }
        summary = ProfessionalSummary(**summary_data)
        assert summary.summary == summary_data["summary"]
        assert summary.highlights == summary_data["highlights"]

    def test_invalid_summary_too_short(self):
        with pytest.raises(ValidationError) as excinfo:
            ProfessionalSummary(summary="Too short")
        assert "summary" in str(
            excinfo.value
        )  # Check that the error is about the 'summary' field

    def test_invalid_highlights_too_many(self):
        highlights = [f"Highlight {i}" for i in range(11)]  # 11 highlights
        with pytest.raises(ValidationError) as excinfo:
            ProfessionalSummary(highlights=highlights)
        assert "highlights" in str(excinfo.value)
        assert "Maximum 10 highlights allowed" in str(excinfo.value)

    def test_invalid_highlight_too_short(self):
        with pytest.raises(ValidationError) as excinfo:
            ProfessionalSummary(highlights=["Too short"])
        assert "Each highlight must be more than 10 characters" in str(excinfo.value)


class TestWorkItem:
    def test_valid_work_item(self):
        item = WorkItem(
            company_name="Test Corp",
            job_title="Tester",
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
            summary="A valid summary that is long enough for validation purposes.",
            highlights=["Did a thing.", "Did another thing."],
        )
        assert item.company_name == "Test Corp"

    def test_end_date_before_start_date(self):
        with pytest.raises(ValidationError) as excinfo:
            WorkItem(
                company_name="Test Corp",
                job_title="Tester",
                start_date=date(2021, 1, 1),
                end_date=date(2020, 1, 1),  # End date before start date
                summary="A valid summary.",
                highlights=["Highlight."],
            )
        assert "End date must be after start date" in str(excinfo.value)

    def test_end_date_present_is_valid(self):
        item = WorkItem(
            company_name="Test Corp",
            job_title="Tester",
            start_date=date(2020, 1, 1),
            end_date="Present",
            summary="A valid summary.",
            highlights=["Highlight."],
        )
        assert item.end_date == "Present"
