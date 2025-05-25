from typing import Optional

from ai.llm import get_cv_improvements
from models.input_cv_fields import CVBody
from models.job_description_fields import JobDescriptionFields
from models.revised_cv_fields import LLMResponse, RevisedCVResponseSchema


def tailor_cv(cv: str, job_description: str):
    response: LLMResponse = get_cv_improvements(job_description, cv)
    if not response.success:
        raise Exception(response.error)
    parsed_response: RevisedCVResponseSchema = response.response.parsed

    # TODO Implement functionality
    pass
