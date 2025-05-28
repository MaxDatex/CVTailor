from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

from models.input_cv_fields import AwardItem as OriginalAwardItem
from models.input_cv_fields import CertificateItem as OriginalCertificateItem
from models.input_cv_fields import CVHeader
from models.input_cv_fields import EducationItem as OriginalEducationItem
from models.input_cv_fields import LanguageItem as OriginalLanguageItem
from models.input_cv_fields import ProjectItem as OriginalProjectItem
from models.input_cv_fields import PublicationItem as OriginalPublicationItem
from models.input_cv_fields import SkillItem as OriginalSkillItem
from models.input_cv_fields import WorkItem as OriginalWorkItem
from models.revised_cv_fields import RevisedSkillItem

T = TypeVar("T")


class ComparisonField(BaseModel, Generic[T]):
    original: T
    suggested: Optional[T] = None


class ComparisonProfessionalSummary(BaseModel):
    summary: ComparisonField[Optional[str]]
    # objective: ComparisonField[Optional[str]]
    highlights: ComparisonField[Optional[List[str]]]


class ComparisonWorkItem(BaseModel):
    id: str
    summary: ComparisonField[str]
    highlights: ComparisonField[List[str]]
    original_data: OriginalWorkItem


class ComparisonProjectItem(BaseModel):
    id: str
    summary: ComparisonField[str]
    highlights: ComparisonField[List[str]]
    original_data: OriginalProjectItem


class ComparisonAwardItem(BaseModel):
    id: str
    summary: ComparisonField[Optional[str]]
    original_data: OriginalAwardItem


class ComparisonPublicationItem(BaseModel):
    id: str
    summary: ComparisonField[Optional[str]]
    original_data: OriginalPublicationItem


class ComparisonCV(BaseModel):
    original_header: CVHeader
    professional_title: ComparisonField[str]
    professional_summary: ComparisonProfessionalSummary
    original_skills: Optional[List[OriginalSkillItem]] = None
    suggested_skills: Optional[List[RevisedSkillItem]] = None

    work_experience: List[ComparisonWorkItem]
    projects: List[ComparisonProjectItem]
    awards: Optional[List[ComparisonAwardItem]] = None
    publications: Optional[List[ComparisonPublicationItem]] = None

    education: Optional[List[OriginalEducationItem]] = None
    certificates: Optional[List[OriginalCertificateItem]] = None
    languages: Optional[List[OriginalLanguageItem]] = None

    ai_general_explanations: str
    ai_suggestions: Optional[str] = None
