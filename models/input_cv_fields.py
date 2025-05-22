from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4


class Location(BaseModel):
    address: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = None
    region: Optional[str] = None


class Profile(BaseModel):
    network: Optional[str] = None
    username: Optional[str] = None
    url: Optional[str] = None


class CVHeader(BaseModel):
    full_name: str
    professional_title: str
    image_url: Optional[str] = None
    email_address: str
    phone_number: str
    github_url: str
    linkedin_url: str
    portfolio_url: Optional[str] = None
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
    company_location: Location
    job_title: str  # Job title
    company_website_url: str  # Company website
    start_date: str  # Format YYYY-MM-DD or YYYY-MM or YYYY
    end_date: str  # Format YYYY-MM-DD or YYYY-MM or YYYY, or Present
    summary: str  # High-level description of role/company
    highlights: List[str]  # Specific achievements or responsibilities (bullet points)


class ProjectItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str  # Project title
    start_date: str
    end_date: str
    description: str  # Overall description of the project
    highlights: List[str]  # Key contributions or features
    url: str  # Link to project demo or repository


class EducationItem(BaseModel):
    institution: str
    url: str
    area: str  # e.g., Computer Science
    study_type: str  # e.g., Bachelor's Degree, Master's
    start_date: str
    end_date: str
    score: str  # e.g., GPA
    courses: List[str]  # Relevant coursework


class AwardItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str
    date: str  # Date awarded
    awarder_by: str  # Organization that gave the award
    summary: str  # Description of the award


class CertificateItem(BaseModel):
    name: str  # Name of the certificate
    date: str  # Date issued
    issuer: str  # Issuing organization (e.g., Coursera, Google)
    url: str  # Link to certificate if available


class PublicationItem(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str  # Title of the publication
    publisher: str  # e.g., Journal name, Conference
    releaseDate: str
    url: str  # Link to publication
    summary: str  # Abstract or brief description


class LanguageItem(BaseModel):
    language: str  # e.g., English, Spanish
    fluency: str  # e.g., Native, Fluent, Conversational


class InterestItem(BaseModel):
    name: str  # Category of interest (e.g., Open Source, AI Ethics)
    keywords: list[str]  # Specific interests


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
