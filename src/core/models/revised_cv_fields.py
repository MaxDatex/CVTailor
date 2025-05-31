from typing import Dict, List, Optional

from google.genai.types import GenerateContentResponse
from pydantic import UUID4, BaseModel, Field, field_validator

from src.core.models.input_cv_fields import ProfessionalSummary, SkillItem


def validate_uuid_id(id: str) -> str:
    """Validates that the provided ID is a valid UUID."""
    if not isinstance(id, str):
        raise TypeError(f"ID {id} should be a string")
    try:
        UUID4(id)
    except ValueError:
        raise ValueError(f"ID {id} should be valid UUID4")
    return id


class RevisedWorkItem(BaseModel):
    """
    Represents a work experience item with AI-suggested revisions.
    Includes minimal identifying fields to link back to the original item.
    """

    id: str = Field(
        ..., description="The unique identifier for the work experience item."
    )
    revised_summary: Optional[str] = Field(
        None, description="AI-suggested revised summary for this work experience."
    )
    revised_highlights: Optional[List[str]] = Field(
        None, description="AI-suggested revised highlights for this work experience."
    )

    validate_id = field_validator("id", mode="before")(validate_uuid_id)


class RevisedProjectItem(BaseModel):
    """
    Represents a project item with AI-suggested revisions.
    Includes minimal identifying fields to link back to the original item.
    """

    id: str = Field(..., description="The unique identifier for the project item.")
    revised_summary: Optional[str] = Field(
        None, description="AI-suggested revised description for the project."
    )
    revised_highlights: Optional[List[str]] = Field(
        None, description="AI-suggested revised highlights for the project."
    )

    validate_id = field_validator("id", mode="before")(validate_uuid_id)


class RevisedAwardItem(BaseModel):
    id: str = Field(..., description="The unique identifier for the award item.")
    revised_summary: Optional[str] = Field(
        None, description="AI-suggested revised summary for the award."
    )

    validate_id = field_validator("id", mode="before")(validate_uuid_id)


class RevisedPublicationItem(BaseModel):
    id: str = Field(..., description="The unique identifier for the publication item.")
    revised_summary: Optional[str] = Field(
        None, description="AI-suggested revised summary for the publication."
    )

    validate_id = field_validator("id", mode="before")(validate_uuid_id)


class RevisedSkillItem(SkillItem):
    pass


class RevisedCVResponseSchema(BaseModel):
    """
    Schema for the AI's response, providing explanations and revised CV sections.
    All revised sections are optional, meaning the AI will only return them
    if it has suggestions for that specific part of the CV.
    """

    explanations: str = Field(
        ..., description="Explanation and plan of changes to the CV."
    )
    revised_professional_title: Optional[str] = Field(
        None, description="AI-suggested revised professional title."
    )
    revised_professional_summary: Optional[ProfessionalSummary] = Field(
        None, description="AI-suggested revised professional summary."
    )
    revised_skills: Optional[List[RevisedSkillItem]] = Field(
        None,
        description="AI-suggested revised skills section. May include rephrased skills or new keywords.",
    )
    revised_work_experience: Optional[List[RevisedWorkItem]] = Field(
        None,
        description="AI-suggested revised work experience items, including revised summaries and highlights.",
    )
    revised_projects: Optional[List[RevisedProjectItem]] = Field(
        None,
        description="AI-suggested revised project items, including revised descriptions and highlights.",
    )
    revised_awards: Optional[List[RevisedAwardItem]] = Field(
        None, description="AI-suggested revised award items."
    )
    revised_publications: Optional[List[RevisedPublicationItem]] = Field(
        None, description="AI-suggested revised publication items."
    )
    suggestions: Optional[str] = Field(
        None, description="Other suggestions for improvements in the CV."
    )


class LLMResponse(BaseModel):
    response: Optional[GenerateContentResponse]
    metadata: Optional[Dict[str, Optional[int]]]
