from typing import Optional, List, Union, TypeVar, Generic
from pydantic import BaseModel
from models.input_cv_fields import (
    ProfessionalSummary as OriginalProfessionalSummary,
    SkillItem as OriginalSkillItem,
    WorkItem as OriginalWorkItem,
    EducationItem as OriginalEducationItem,
    ProjectItem as OriginalProjectItem,
    AwardItem as OriginalAwardItem,
    PublicationItem as OriginalPublicationItem,
    CVHeader # Keep original header parts that are not revised by AI
)
from models.revised_cv_fields import (
    RevisedWorkItem, # AI gives a subset of fields for these
    RevisedProjectItem,
    RevisedAwardItem,
    RevisedPublicationItem,
    RevisedSkillItem
)


T = TypeVar('T')

class ComparisonField(BaseModel, Generic[T]):
    original: T
    suggested: Optional[T] = None
    # ai_explanation_snippet: Optional[str] = None # Optional: A snippet from RevisedCVResponseSchema.explanations relevant to this field


class ComparisonProfessionalSummary(BaseModel):
    summary: ComparisonField[Optional[str]]
    objective: ComparisonField[Optional[str]]
    highlights: ComparisonField[Optional[List[str]]]


class ComparisonWorkItem(BaseModel):
    id: str
    # company_name: str
    # job_title_original: str

    # Compared fields
    summary: ComparisonField[str]
    highlights: ComparisonField[List[str]]

    # Other original fields (not revised by AI but needed for display)
    # e.g., company_location, company_website_url, start_date, end_date
    original_data: OriginalWorkItem # Keep the full original item for unrevised parts

class ComparisonProjectItem(BaseModel):
    id: str
    # name_original: str
    summary: ComparisonField[str]
    highlights: ComparisonField[List[str]]
    original_data: OriginalProjectItem

class ComparisonAwardItem(BaseModel):
    id: str
    summary: ComparisonField[str]
    original_data: OriginalAwardItem

class ComparisonPublicationItem(BaseModel):
    id: str
    summary: ComparisonField[Optional[str]]
    original_data: OriginalPublicationItem

# ... similar structures for ComparisonAwardItem, ComparisonPublicationItem

class ComparisonCV(BaseModel):
    # Fields from CVHeader that aren't directly revised by AI
    # but you might still want to show them.
    # Or, the header itself could be a ComparisonField if parts are revised.
    original_header: CVHeader # For now, assume header parts like name, email are not AI-revised

    # Revised fields
    professional_title: ComparisonField[str]
    professional_summary: ComparisonProfessionalSummary
    original_skills: Optional[List[OriginalSkillItem]] = None
    suggested_skills: Optional[List[RevisedSkillItem]] = None

    work_experience: List[ComparisonWorkItem]
    projects: List[ComparisonProjectItem]
    awards: Optional[List[ComparisonAwardItem]] = None
    publications: Optional[List[ComparisonPublicationItem]] = None

    # Sections not revised by AI (directly pass through from original CVBody)
    education: Optional[List[OriginalEducationItem]] = None # Assuming Education is not revised by current AI prompt
    # ... other non-revised sections like languages, certificates

    ai_general_explanations: str # From RevisedCVResponseSchema.explanations