from typing import Optional
from models.input_cv_fields import CVBody
from models.job_description_fields import JobDescriptionFields
from models.revised_cv_fields import TestResponseSchema
from ai.llm import get_cv_improvements

def tailor_cv(cv: CVBody, job_description: JobDescriptionFields):
    response = get_cv_improvements(job_description, cv)
    # TODO Implement functionality
    pass

