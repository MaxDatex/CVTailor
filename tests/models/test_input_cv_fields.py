from datetime import date
from typing import List

import pytest
from pydantic import AnyUrl, ValidationError

from src.core.models.input_cv_fields import (
    AwardItem,
    CertificateItem,
    CVHeader,
    EducationItem,
    LanguageFluency,
    LanguageItem,
    Location,
    ProfessionalSummary,
    Profile,
    ProjectItem,
    PublicationItem,
    SkillItem,
    SkillLevel,
    StudyType,
    WorkItem,
    validate_highlights_list,
    validate_keywords_list,
)


class TestHighlightsValidators:
    def test_validate_highlights_list_valid(self):
        highlights = ["This is a valid highlight over ten chars."]
        assert validate_highlights_list(highlights) == highlights

    def test_validate_highlights_list_empty(self):
        assert validate_highlights_list([]) == []

    def test_validate_highlights_list_none_input(self):
        assert validate_highlights_list([]) == []

    def test_validate_highlights_list_too_many(self):
        highlights = ["Valid highlight " + str(i) for i in range(11)]
        with pytest.raises(ValueError, match="Maximum 10 highlights allowed"):
            validate_highlights_list(highlights)

    def test_validate_highlights_list_item_too_short(self):
        highlights = ["short"]
        with pytest.raises(
            ValueError, match="Each highlight must be more than 10 characters"
        ):
            validate_highlights_list(highlights)

    def test_validate_highlights_list_item_too_long(self):
        highlights = ["a" * 201]
        with pytest.raises(
            ValueError, match="Each highlight must be less than 200 characters"
        ):
            validate_highlights_list(highlights)


class TestKeywordsValidators:
    def test_validate_keywords_list_valid(self):
        keywords = ["python", "data science"]
        assert validate_keywords_list(keywords) == keywords

    def test_validate_keywords_list_empty(self):
        assert validate_keywords_list([]) == []

    def test_validate_keywords_list_too_many(self):
        keywords = ["keyword" + str(i) for i in range(21)]
        with pytest.raises(ValueError, match="Maximum 20 keywords allowed"):
            validate_keywords_list(keywords)

    def test_validate_keywords_list_item_too_short(self):
        keywords = [""]  # Empty string keyword
        with pytest.raises(
            ValueError, match="Each keyword must be more than 1 characters"
        ):
            validate_keywords_list(keywords)

    def test_validate_keywords_list_item_too_long(self):
        keywords = ["a" * 51]
        with pytest.raises(
            ValueError, match="Each keyword must be less than 50 characters"
        ):
            validate_keywords_list(keywords)


class TestLocation:
    def test_location_valid(self):
        data = {"city": "Kyiv", "countryCode": "UA"}
        loc = Location(**data)
        assert loc.city == "Kyiv"
        assert loc.countryCode == "UA"

    def test_location_optional_fields(self):
        loc = Location(city="Lviv")
        assert loc.city == "Lviv"
        assert loc.address is None

    def test_location_field_min_length(self):
        with pytest.raises(ValidationError):
            Location(city="A")


class TestProfile:
    def test_profile_valid(self):
        data = {
            "network": "GitHub",
            "username": "user123",
            "url": "http://github.com/user123",
        }
        prof = Profile(**data)
        assert prof.network == "GitHub"
        assert isinstance(prof.url, AnyUrl)

    def test_profile_invalid_url(self):
        with pytest.raises(ValidationError):
            Profile(network="Test", username="test", url="not a url")


class TestCVHeader:
    def test_cv_header_valid(self):
        data = {
            "full_name": "John Doe",
            "professional_title": "Software Engineer",
            "email_address": "john.doe@example.com",
            "phone_number": "+12025550104",
            "github_url": "https://github.com/johndoe",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "location": {"city": "Testville"},
        }
        header = CVHeader(**data)
        assert header.full_name == "John Doe"
        assert isinstance(header.phone_number, str)
        assert header.location.city == "Testville"

    def test_cv_header_missing_required_field(self):
        with pytest.raises(ValidationError) as excinfo:
            CVHeader(professional_title="Dev")  # Missing full_name, email, phone, etc.
        # Check for one of the missing fields
        assert "full_name" in str(excinfo.value).lower()

    def test_cv_header_invalid_email(self):
        with pytest.raises(ValidationError):
            CVHeader(
                full_name="Jane Doe",
                professional_title="QA",
                email_address="not-an-email",
                phone_number="+12025550104",
                github_url="https://github.com/johndoe",
                linkedin_url="https://linkedin.com/in/johndoe",
            )


class TestProfessionalSummary:
    def test_valid_summary(self, valid_summary_data, valid_highlights_data):
        summary = ProfessionalSummary(
            summary=valid_summary_data, highlights=valid_highlights_data
        )
        assert summary.summary == valid_summary_data
        assert summary.highlights == valid_highlights_data

    def test_invalid_summary_too_short(self):
        with pytest.raises(ValidationError) as excinfo:
            ProfessionalSummary(summary="Too short")
        assert "summary" in str(excinfo.value)

    def test_invalid_highlights_too_many(self, valid_summary_data):
        highlights = [f"Highlight {i}" for i in range(11)]  # 11 highlights
        with pytest.raises(ValidationError) as excinfo:
            ProfessionalSummary(summary=valid_summary_data, highlights=highlights)
        assert "highlights" in str(excinfo.value)
        assert "Maximum 10 highlights allowed" in str(excinfo.value)

    def test_invalid_highlight_too_short(self, valid_summary_data):
        with pytest.raises(ValidationError) as excinfo:
            ProfessionalSummary(summary=valid_summary_data, highlights=["Too short"])
        assert "Each highlight must be more than 10 characters" in str(excinfo.value)


class TestSkillItem:
    def test_skill_item_valid(self):
        data = {
            "name": "Python",
            "level": SkillLevel.ADVANCED,
            "keywords": ["scripting", "OOP"],
        }
        skill = SkillItem(**data)
        assert skill.name == "Python"
        assert skill.level == SkillLevel.ADVANCED

    def test_skill_item_invalid_level(self):
        with pytest.raises(ValidationError):
            SkillItem(name="Java", level="GodTier", keywords=["enterprise"])

    def test_skill_item_too_many_keywords(self):
        with pytest.raises(ValidationError, match="Maximum 20 keywords allowed"):
            SkillItem(
                name="Too Many",
                level=SkillLevel.BEGINNER,
                keywords=[f"k{i}" for i in range(21)],
            )

    def test_skill_item_keyword_too_short(self):
        with pytest.raises(
            ValidationError, match="Each keyword must be more than 1 characters"
        ):
            SkillItem(
                name="Short Keyword", level=SkillLevel.INTERMEDIATE, keywords=[""]
            )

    def test_skill_item_keyword_too_long(self):
        with pytest.raises(
            ValidationError, match="Each keyword must be less than 50 characters"
        ):
            SkillItem(name="Long Keyword", level=SkillLevel.EXPERT, keywords=["a" * 51])

    def test_skill_item_empty_keywords_list_is_valid(self):
        skill = SkillItem(name="No Keywords", level=SkillLevel.BEGINNER, keywords=[])
        assert skill.keywords == []


class TestWorkItem:
    def test_valid_work_item(
        self, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        item = WorkItem(
            company_name="Test Corp",
            company_location=None,
            job_title="Tester",
            company_website_url=None,
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
            summary=valid_summary_data,
            highlights=valid_highlights_data,
        )
        assert item.company_name == "Test Corp"

    def test_end_date_before_start_date(
        self, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        with pytest.raises(ValidationError) as excinfo:
            WorkItem(
                company_name="Test Corp",
                company_location=None,
                job_title="Tester",
                company_website_url=None,
                start_date=date(2021, 1, 1),
                end_date=date(2020, 1, 1),  # End date before start date
                summary=valid_summary_data,
                highlights=valid_highlights_data,
            )
        assert "End date must be after start date" in str(excinfo.value)

    def test_end_date_present_is_valid(
        self, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        item = WorkItem(
            company_name="Test Corp",
            company_location=None,
            job_title="Tester",
            company_website_url=None,
            start_date=date(2020, 1, 1),
            end_date="Present",
            summary=valid_summary_data,
            highlights=valid_highlights_data,
        )
        assert item.end_date == "Present"


class TestProjectItem:
    def test_project_item_valid(
        self, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        data = {
            "name": "AI Chatbot",
            "summary": valid_summary_data,
            "highlights": valid_highlights_data,
        }
        project = ProjectItem(**data)
        assert project.name == "AI Chatbot"

    def test_project_item_end_date_validation(
        self, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        with pytest.raises(ValidationError, match="End date must be after start date"):
            ProjectItem(
                name="Test Project",
                start_date=date(2022, 1, 1),
                end_date=date(2021, 1, 1),  # Invalid
                summary=valid_summary_data,
                highlights=valid_highlights_data,
                url=None,
            )

    def test_project_item_too_many_highlights(self, valid_summary_data: str):
        with pytest.raises(ValidationError, match="Maximum 10 highlights allowed"):
            ProjectItem(
                name="Too Many Highlights",
                summary=valid_summary_data,
                highlights=[f"Highlight {i} is clearly valid." for i in range(11)],
            )

    def test_project_item_highlight_too_short(self, valid_summary_data: str):
        with pytest.raises(
            ValidationError, match="Each highlight must be more than 10 characters"
        ):
            ProjectItem(
                name="Short Highlight", summary=valid_summary_data, highlights=["short"]
            )

    def test_project_item_highlight_too_long(self, valid_summary_data: str):
        with pytest.raises(
            ValidationError, match="Each highlight must be less than 200 characters"
        ):
            ProjectItem(
                name="Long Highlight",
                summary=valid_summary_data,
                highlights=["a" * 201],
            )

    def test_project_item_empty_highlights_list_is_valid(self, valid_summary_data):
        project = ProjectItem(
            name="No Highlights", summary=valid_summary_data, highlights=[]
        )
        assert project.highlights == []


class TestEducationItem:
    def test_education_item_valid(self):
        data = {
            "institution": "University of Example",
            "area": "Computer Science",
            "study_type": StudyType.BACHELORS,
            "start_date": date(2018, 9, 1),
            "end_date": date(2022, 6, 30),
            "courses": ["Data Structures", "Algorithms"],
        }
        edu = EducationItem(**data)
        assert edu.institution == "University of Example"

    def test_education_item_invalid_study_type(self):
        with pytest.raises(ValidationError):
            EducationItem(
                institution="Fake School",
                area="Art",
                study_type="Associate",  # Invalid
                start_date=date(2020, 1, 1),
                end_date=date(2022, 1, 1),
                courses=[],
            )


class TestAwardItem:
    def test_award_item_valid(self, valid_summary_data: str):
        data = {
            "title": "Best Project Award",
            "date": date(2023, 5, 15),
            "summary": valid_summary_data,
        }
        award = AwardItem(**data)
        assert award.title == "Best Project Award"
        assert award.summary is not None

    def test_award_item_summary_optional(self):
        data = {"title": "Participation Prize", "date": date(2023, 1, 1)}
        award = AwardItem(**data)
        assert award.summary is None


class TestCertificateItem:
    def test_certificate_item_valid(self):
        data = {
            "name": "Certified Kubernetes Administrator",
            "date": date(2023, 10, 1),
            "issuer": "Cloud Native Computing Foundation",
        }
        cert = CertificateItem(**data)
        assert cert.name == "Certified Kubernetes Administrator"


class TestPublicationItem:
    def test_publication_item_valid(self, valid_summary_data: str):
        data = {
            "name": "Advanced Techniques in ML",
            "publisher": "Tech Press",
            "releaseDate": date(2023, 7, 20),
            "summary": valid_summary_data,
        }
        pub = PublicationItem(**data)
        assert pub.name == "Advanced Techniques in ML"


class TestLanguageItem:
    def test_language_item_valid(self):
        data = {"language": "Spanish", "fluency": LanguageFluency.FLUENT}
        lang = LanguageItem(**data)
        assert lang.language == "Spanish"

    def test_language_item_invalid_fluency(self):
        with pytest.raises(ValidationError):
            LanguageItem(language="Klingon", fluency="Conversational")
