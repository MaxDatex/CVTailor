from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field, AnyUrl
from pydantic_extra_types.phone_numbers import PhoneNumber
from uuid import uuid4
from datetime import date as dtdate


class Location(BaseModel):
    address: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = None
    region: Optional[str] = None


class Profile(BaseModel):
    network: Optional[str] = None
    username: Optional[str] = None
    url: Optional[AnyUrl] = None


class CVHeader(BaseModel):
    full_name: str
    professional_title: str
    image_url: Optional[str] = None
    email_address: str
    phone_number: PhoneNumber
    github_url: AnyUrl
    linkedin_url: AnyUrl
    portfolio_url: Optional[AnyUrl] = None
    location: Optional[Location] = None
    profiles: Optional[List[Profile]] = None


class ProfessionalSummary(BaseModel):
    summary: Optional[str] = None
    objective: Optional[str] = None
    highlights: Optional[List[str]] = None


class SkillItem(BaseModel):
    name: str  # Broad skill category (e.g., Web Development, Data Science)
    level: str  # Optional proficiency level (e.g., Intermediate, Advanced)
    keywords: List[str]  # Specific technologies or tools (e.g., Python, PyTorch, AWS)


class WorkItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    company_name: str  # Name of the company/organization
    company_location: Optional[Location]
    job_title: str  # Job title
    company_website_url: Optional[AnyUrl]  # Company website
    start_date: dtdate
    end_date: Union[dtdate, Literal['Present']] = 'Present'
    summary: str  # High-level description of role/company
    highlights: List[str]  # Specific achievements or responsibilities (bullet points)


class ProjectItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str  # Project title
    start_date: Optional[dtdate]
    end_date: Optional[Union[dtdate, Literal['Present']]]
    description: str  # Overall description of the project
    highlights: List[str]  # Key contributions or features
    url: Optional[AnyUrl]  # Link to project demo or repository


class EducationItem(BaseModel):
    institution: str
    url: Optional[AnyUrl]
    area: str  # e.g., Computer Science
    study_type: str  # e.g., Bachelor's Degree, Master's
    start_date: dtdate
    end_date: Union[dtdate, Literal['Present']]
    score: str  # e.g., GPA
    courses: List[str]  # Relevant coursework


class AwardItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str
    date: dtdate  # Date awarded
    awarder_by: Optional[str]  # Organization that gave the award
    summary: Optional[str]  # Description of the award


class CertificateItem(BaseModel):
    name: str  # Name of the certificate
    date: dtdate  # Date issued
    issuer: str  # Issuing organization (e.g., Coursera, Google)
    url: Optional[AnyUrl]  # Link to certificate if available


class PublicationItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str  # Title of the publication
    publisher: str  # e.g., Journal name, Conference
    releaseDate: dtdate
    url: Optional[AnyUrl]  # Link to publication
    summary: str  # Abstract or brief description


class LanguageItem(BaseModel):
    language: str  # e.g., English, Spanish
    fluency: str  # e.g., Native, Fluent, Conversational


class InterestItem(BaseModel):
    name: str  # Category of interest (e.g., Open Source, AI Ethics)
    keywords: List[str]  # Specific interests


class ReferenceItem(BaseModel):
    name: str  # Name of reference (ensure consent)
    reference: str  # Testimonial or contact details (handle privacy appropriately)


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
