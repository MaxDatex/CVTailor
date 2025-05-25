from typing import Dict, List, Optional, Union

from google.genai.types import GenerateContentResponse
from pydantic import BaseModel, Field

from models.input_cv_fields import ProfessionalSummary, SkillItem


class RevisedWorkItem(BaseModel):
    """
    Represents a work experience item with AI-suggested revisions.
    Includes minimal identifying fields to link back to the original item.
    """

    id: str = Field(
        ..., description="The unique identifier for the work experience item."
    )
    # company_name: str = Field(
    #     ..., description="The name of the company/organization for identification."
    # )
    # job_title: str = Field(..., description="The job title for identification.")
    revised_summary: Optional[str] = Field(
        None, description="AI-suggested revised summary for this work experience."
    )
    revised_highlights: Optional[List[str]] = Field(
        None, description="AI-suggested revised highlights for this work experience."
    )


class RevisedProjectItem(BaseModel):
    """
    Represents a project item with AI-suggested revisions.
    Includes minimal identifying fields to link back to the original item.
    """

    id: str = Field(..., description="The unique identifier for the project item.")
    # name: str = Field(..., description="The project title for identification.")
    revised_summary: Optional[str] = Field(
        None, description="AI-suggested revised description for the project."
    )
    revised_highlights: Optional[List[str]] = Field(
        None, description="AI-suggested revised highlights for the project."
    )


class RevisedAwardItem(BaseModel):
    id: str = Field(..., description="The unique identifier for the award item.")
    # title: str = Field(..., description="The award title for identification.")
    revised_summary: Optional[str] = Field(
        None, description="AI-suggested revised summary for the award."
    )


class RevisedPublicationItem(BaseModel):
    id: str = Field(..., description="The unique identifier for the publication item.")
    # name: str = Field(..., description="The publication title for identification.")
    revised_summary: Optional[str] = Field(
        None, description="AI-suggested revised summary for the publication."
    )


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
    metadata: Optional[Dict[str, Union[int, None]]]
