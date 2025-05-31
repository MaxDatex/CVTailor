from src.core.models.input_cv_fields import CVBody
from src.core.models.job_description_fields import JobDescriptionFields
from src.core.templates.md_cv_template_to_llm import CV_TEMPLATE_LLM_MD
from loguru import logger
from jinja2 import Template

from src.core.templates.md_job_description_template import JOB_DESCRIPTION_TEMPLATE_MD


class TemplateLLMRenderer:
    @staticmethod
    def cv_to_llm_format(cv: CVBody) -> str:
        """Transform CV to LLM-readable format"""
        cv_template = Template(CV_TEMPLATE_LLM_MD)
        rendered_cv = cv_template.render(cv=cv)
        logger.info(f"CV for LLM content: {rendered_cv[:100]}")
        return rendered_cv

    @staticmethod
    def job_description_to_llm_format(job_description: JobDescriptionFields) -> str:
        """Transform job description to LLM-readable format"""
        job_description_template = Template(JOB_DESCRIPTION_TEMPLATE_MD)
        rendered_job_description = job_description_template.render(job_description_data=job_description)
        logger.info(f"Job description for LLM content: {rendered_job_description[:100]}")
        return rendered_job_description
