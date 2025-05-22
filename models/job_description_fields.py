from typing import Optional

from pydantic import BaseModel, Field


class JobDescriptionContent(BaseModel):
    about_company: Optional[str] = Field(None, max_length=2000)
    about_role: Optional[str] = Field(None, max_length=2000)
    requirements: Optional[str] = Field(None, max_length=2000)
    nice_to_have: Optional[str] = Field(None, max_length=2000)
    responsibilities: Optional[str] = Field(None, max_length=2000)
    other: Optional[str] = Field(None, max_length=1000)

    class Config:
        validate_assignment = True


class JobDescriptionFields(BaseModel):
    job_title: str
    job_description: JobDescriptionContent
