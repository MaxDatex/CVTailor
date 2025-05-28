from datetime import date as dtdate
from enum import Enum
from typing import List, Literal, Optional, Union
from uuid import uuid4

from pydantic import (AnyUrl, BaseModel, EmailStr, Field, ValidationInfo,
                      field_validator)
from pydantic_extra_types.phone_numbers import PhoneNumber


def validate_highlights_list(highlights: List[str]) -> List[str]:
    """
    Validates a list of highlights for count, and individual length.
    """
    if not highlights:
        return []
    if len(highlights) > 10:
        raise ValueError("Maximum 10 highlights allowed")
    if any(len(highlight) < 10 for highlight in highlights):
        raise ValueError("Each highlight must be more than 10 characters")
    if any(len(highlight) > 200 for highlight in highlights):
        raise ValueError("Each highlight must be less than 200 characters")
    return highlights


def validate_keywords_list(keywords: List[str]) -> List[str]:
    """
    Validates a list of keywords for count, and individual length.
    """
    if not keywords:
        return []
    if len(keywords) > 20:
        raise ValueError("Maximum 20 keywords allowed")
    if any(len(keyword) < 1 for keyword in keywords):
        raise ValueError("Each keyword must be more than 1 characters")
    if any(len(keyword) > 50 for keyword in keywords):
        raise ValueError("Each keyword must be less than 50 characters")
    return keywords


def validate_end_date(
    end_date: dtdate, info: ValidationInfo
) -> Union[dtdate, Literal["Present"]]:
    """
    Validates that the end date is after the start date.
    """
    if end_date is None or info.data.get("start_date") is None:
        return end_date

    if end_date != "Present" and end_date < info.data.get("start_date"):
        raise ValueError("End date must be after start date")
    return end_date


class Location(BaseModel):
    address: Optional[str] = Field(None, min_length=2, max_length=100)
    postalCode: Optional[str] = Field(None, min_length=2, max_length=50)
    city: Optional[str] = Field(None, min_length=2, max_length=500)
    countryCode: Optional[str] = Field(None, min_length=2, max_length=50)
    region: Optional[str] = Field(None, min_length=2, max_length=500)


class Profile(BaseModel):
    network: Optional[str] = Field(None, min_length=1, max_length=100)
    username: Optional[str] = Field(None, min_length=1, max_length=100)
    url: Optional[AnyUrl] = None


class CVHeader(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    professional_title: str = Field(..., min_length=2, max_length=100)
    image_url: Optional[str] = None
    email_address: EmailStr
    phone_number: PhoneNumber
    github_url: AnyUrl
    linkedin_url: AnyUrl
    portfolio_url: Optional[AnyUrl] = None
    location: Optional[Location] = None
    profiles: Optional[List[Profile]] = None


class ProfessionalSummary(BaseModel):
    summary: str = Field(..., min_length=50, max_length=5000)
    # objective: Optional[str] = Field(None, min_length=50, max_length=5000)
    highlights: Optional[List[str]] = None

    validate_highlights = field_validator("highlights")(validate_highlights_list)

    model_config = {
        "validate_assignment": True,
    }


class SkillLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class SkillItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    level: SkillLevel
    keywords: List[str]

    validate_keywords = field_validator("keywords")(validate_keywords_list)

    model_config = {
        "validate_assignment": True,
    }


class WorkItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    company_name: str = Field(..., min_length=1, max_length=100)
    company_location: Optional[Location] = None
    job_title: str = Field(..., min_length=1, max_length=100)
    company_website_url: Optional[AnyUrl] = None
    start_date: dtdate
    end_date: Union[dtdate, Literal["Present"]] = "Present"
    summary: str = Field(..., min_length=50, max_length=5000)
    highlights: List[str]

    validate_highlights = field_validator("highlights")(validate_highlights_list)
    validate_date = field_validator("end_date")(validate_end_date)

    model_config = {
        "validate_assignment": True,
    }


class ProjectItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str = Field(..., min_length=1, max_length=100)
    start_date: Optional[dtdate] = None
    end_date: Optional[Union[dtdate, Literal["Present"]]] = None
    summary: str = Field(..., min_length=50, max_length=5000)
    highlights: List[str]
    url: Optional[AnyUrl] = None

    validate_highlights = field_validator("highlights")(validate_highlights_list)
    validate_date = field_validator("end_date")(validate_end_date)

    model_config = {
        "validate_assignment": True,
    }


class StudyType(str, Enum):
    HIGH_SCHOOL = "High School"
    BACHELORS = "Bachelors"
    MASTERS = "Masters"
    PHD = "PhD"


class EducationItem(BaseModel):
    institution: str = Field(..., min_length=1, max_length=100)
    url: Optional[AnyUrl] = None
    area: str = Field(..., min_length=2, max_length=100)  # e.g., Computer Science
    study_type: StudyType
    start_date: dtdate
    end_date: Union[dtdate, Literal["Present"]]
    score: Optional[Union[str, float]] = None
    courses: Optional[List[str]] = None

    validate_date = field_validator("end_date")(validate_end_date)

    model_config = {
        "validate_assignment": True,
    }


class AwardItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str = Field(..., min_length=1, max_length=100)
    date: dtdate
    awarder_by: Optional[str] = Field(None, min_length=2, max_length=100)
    summary: Optional[str] = Field(None, min_length=50, max_length=5000)


class CertificateItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    date: dtdate
    issuer: str = Field(..., min_length=1, max_length=100)
    url: Optional[AnyUrl] = None


class PublicationItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str = Field(..., min_length=1, max_length=100)
    publisher: Optional[str] = Field(None, min_length=1, max_length=100)
    releaseDate: dtdate
    url: Optional[AnyUrl] = None
    summary: str = Field(..., min_length=50, max_length=5000)


class LanguageFluency(str, Enum):
    NATIVE = "Native"
    FLUENT = "Fluent"
    UPPER_INTERMEDIATE = "Upper Intermediate"
    INTERMEDIATE = "Intermediate"
    BASIC = "Basic"


class LanguageItem(BaseModel):
    language: str = Field(..., min_length=2, max_length=100)
    fluency: LanguageFluency


class InterestItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    keywords: List[str]

    validate_keywords = field_validator("keywords")(validate_keywords_list)

    model_config = {
        "validate_assignment": True,
    }


class ReferenceItem(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    reference: str = Field(..., min_length=50, max_length=5000)


class CVBody(BaseModel):
    header: CVHeader
    professional_summary: ProfessionalSummary
    skills: Optional[List[SkillItem]] = None
    work_experience: Optional[List[WorkItem]] = None
    projects: Optional[List[ProjectItem]] = None
    education: Optional[List[EducationItem]] = None
    awards: Optional[List[AwardItem]] = None
    certificates: Optional[List[CertificateItem]] = None
    publications: Optional[List[PublicationItem]] = None
    languages: Optional[List[LanguageItem]] = None
