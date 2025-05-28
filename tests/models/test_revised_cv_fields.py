from typing import List
from unittest.mock import MagicMock

import pytest
from google.genai.types import GenerateContentResponse
from pydantic import ValidationError
from pydantic.v1 import UUID4

from src.core.models.input_cv_fields import ProfessionalSummary, SkillLevel
from src.core.models.revised_cv_fields import (
    LLMResponse,
    RevisedAwardItem,
    RevisedCVResponseSchema,
    RevisedProjectItem,
    RevisedPublicationItem,
    RevisedSkillItem,
    RevisedWorkItem,
)
from tests.conftest import valid_summary_data


class TestRevisedWorkItem:
    def test_valid_instantiation_all_fields(
        self, valid_summary_data: str, valid_highlights_data: List[str], valid_id: UUID4
    ):
        item = RevisedWorkItem(
            id=valid_id,
            revised_summary=valid_summary_data,
            revised_highlights=valid_highlights_data,
        )
        assert item.id == valid_id
        assert item.revised_summary == valid_summary_data
        assert item.revised_highlights == valid_highlights_data

    def test_valid_instantiation_optional_fields_missing(self, valid_id: UUID4):
        data = {"id": valid_id}
        item = RevisedWorkItem(**data)
        assert item.id == valid_id
        assert item.revised_summary is None
        assert item.revised_highlights is None

    def test_missing_required_id(
        self, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        with pytest.raises(ValidationError) as excinfo:
            RevisedWorkItem(
                revised_summary=valid_summary_data,
                revised_highlights=valid_highlights_data,
            )
        assert "id" in str(excinfo.value).lower()

    def test_invalid_id_type(
        self, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        with pytest.raises(ValidationError) as excinfo:
            RevisedWorkItem(
                id=123,
                revised_summary=valid_summary_data,
                revised_highlights=valid_highlights_data,
            )
        assert "id" in str(excinfo.value).lower()

    def test_optional_fields_can_be_empty_list(self, valid_id: str):
        data = {"id": valid_id, "revised_highlights": []}
        item = RevisedWorkItem(**data)
        assert item.revised_highlights == []
        assert item.revised_summary is None


class TestRevisedProjectItem:
    def test_valid_instantiation_all_fields(
        self, valid_id: str, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        item = RevisedProjectItem(
            id=valid_id,
            revised_summary=valid_summary_data,
            revised_highlights=valid_highlights_data,
        )
        assert item.id == valid_id
        assert item.revised_summary == valid_summary_data
        assert item.revised_highlights == valid_highlights_data

    def test_valid_instantiation_optional_fields_missing(self, valid_id: str):
        item = RevisedProjectItem(id=valid_id)
        assert item.id == valid_id
        assert item.revised_summary is None
        assert item.revised_highlights is None

    def test_missing_required_id(self, valid_summary_data: str):
        with pytest.raises(ValidationError):
            RevisedProjectItem(revised_summary=valid_summary_data)


class TestRevisedAwardItem:
    def test_valid_instantiation(self, valid_id: str, valid_summary_data: str):
        item = RevisedAwardItem(id=valid_id, revised_summary=valid_summary_data)
        assert item.id == valid_id
        assert item.revised_summary == valid_summary_data

    def test_valid_instantiation_summary_missing(self, valid_id: str):
        item = RevisedAwardItem(id=valid_id)
        assert item.id == valid_id
        assert item.revised_summary is None

    def test_missing_required_id(self, valid_summary_data: str):
        with pytest.raises(ValidationError):
            RevisedAwardItem(revised_summary=valid_summary_data)


class TestRevisedPublicationItem:
    def test_valid_instantiation(self, valid_id: str, valid_summary_data: str):
        item = RevisedPublicationItem(id=valid_id, revised_summary=valid_summary_data)
        assert item.id == valid_id
        assert item.revised_summary == valid_summary_data

    def test_valid_instantiation_summary_missing(self, valid_id: str):
        item = RevisedPublicationItem(id=valid_id)
        assert item.id == valid_id
        assert item.revised_summary is None

    def test_missing_required_id(self, valid_summary_data: str):
        with pytest.raises(ValidationError):
            RevisedPublicationItem(revised_summary=valid_summary_data)


class TestRevisedSkillItem:
    def test_valid_instantiation_inherited(self):
        data = {
            "name": "Async Python",
            "level": SkillLevel.ADVANCED,
            "keywords": ["asyncio", "await", "coroutines"],
        }
        item = RevisedSkillItem(**data)
        assert item.name == "Async Python"
        assert item.level == SkillLevel.ADVANCED
        assert item.keywords == ["asyncio", "await", "coroutines"]

    def test_invalid_keyword_inherited_validation(self):
        with pytest.raises(ValidationError, match="Maximum 20 keywords allowed"):
            RevisedSkillItem(
                name="Too Many Keywords",
                level=SkillLevel.EXPERT,
                keywords=[f"k{i}" for i in range(21)],
            )


class TestRevisedCVResponseSchema:
    def test_valid_instantiation_minimal(self):
        data = {"explanations": "Minimal changes applied."}
        schema = RevisedCVResponseSchema(**data)
        assert schema.explanations == "Minimal changes applied."
        assert schema.revised_professional_title is None
        assert schema.revised_professional_summary is None
        assert schema.revised_skills is None
        assert schema.revised_work_experience is None
        assert schema.revised_projects is None
        assert schema.revised_awards is None
        assert schema.revised_publications is None
        assert schema.suggestions is None

    def test_valid_instantiation_all_fields(
        self, valid_id: str, valid_summary_data: str, valid_highlights_data: List[str]
    ):
        ps_data = {"summary": valid_summary_data, "highlights": valid_highlights_data}
        skill_data = {
            "name": "Python",
            "level": SkillLevel.ADVANCED,
            "keywords": ["general", "purpose"],
        }

        data = {
            "explanations": "Comprehensive review and revisions.",
            "revised_professional_title": "Chief Innovator",
            "revised_professional_summary": ps_data,
            "revised_skills": [skill_data],
            "revised_work_experience": [
                {"id": valid_id, "revised_summary": valid_summary_data}
            ],
            "revised_projects": [
                {"id": valid_id, "revised_summary": valid_summary_data}
            ],
            "revised_awards": [{"id": valid_id, "revised_summary": valid_summary_data}],
            "revised_publications": [
                {"id": valid_id, "revised_summary": valid_summary_data}
            ],
            "suggestions": "Consider adding a section on volunteer experience.",
        }
        schema = RevisedCVResponseSchema(**data)
        assert schema.explanations == "Comprehensive review and revisions."
        assert schema.revised_professional_title == "Chief Innovator"
        assert isinstance(schema.revised_professional_summary, ProfessionalSummary)
        assert schema.revised_professional_summary.summary == valid_summary_data
        assert len(schema.revised_skills) == 1
        assert isinstance(schema.revised_skills[0], RevisedSkillItem)
        assert schema.revised_skills[0].name == "Python"
        assert len(schema.revised_work_experience) == 1
        assert schema.revised_work_experience[0].id == valid_id

    def test_missing_required_explanations(self):
        with pytest.raises(ValidationError) as excinfo:
            RevisedCVResponseSchema(revised_professional_title="New Title")
        assert "explanations" in str(excinfo.value).lower()

    def test_nested_model_validation_professional_summary(self):
        invalid_ps_data = {"summary": "short"}
        data = {
            "explanations": "Testing nested validation.",
            "revised_professional_summary": invalid_ps_data,
        }
        with pytest.raises(ValidationError) as excinfo:
            RevisedCVResponseSchema(**data)
        assert "revised_professional_summary" in str(excinfo.value).lower()
        assert "summary" in str(excinfo.value).lower()
        assert "50 characters" in str(excinfo.value)

    def test_nested_model_validation_revised_skills(self):
        invalid_skill_data = {"name": "Bad Skill", "level": "Superstar", "keywords": []}
        data = {
            "explanations": "Testing nested skill validation.",
            "revised_skills": [invalid_skill_data],
        }
        with pytest.raises(ValidationError) as excinfo:
            RevisedCVResponseSchema(**data)
        assert "revised_skills" in str(excinfo.value).lower()
        assert "level" in str(excinfo.value).lower()


class TestLLMResponse:
    def test_valid_instantiation(self):
        mock_gen_content_response = MagicMock(spec=GenerateContentResponse)
        mock_gen_content_response.parsed = {"key": "value"}

        metadata_dict = {"input_tokens_count": 100, "output_tokens_count": 200}

        llm_response = LLMResponse(
            response=mock_gen_content_response, metadata=metadata_dict
        )

        assert llm_response.response == mock_gen_content_response
        assert llm_response.metadata == metadata_dict

    def test_optional_fields_missing(self):
        llm_response = LLMResponse(response=None, metadata=None)
        assert llm_response.response is None
        assert llm_response.metadata is None

    def test_metadata_values_can_be_none(self):
        mock_gen_content_response = MagicMock(spec=GenerateContentResponse)
        metadata_with_nones = {"input_tokens_count": 100, "output_tokens_count": None}
        llm_response = LLMResponse(
            response=mock_gen_content_response, metadata=metadata_with_nones
        )
        assert llm_response.metadata["output_tokens_count"] is None
