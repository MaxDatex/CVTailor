from typing import Any, Tuple, Type

from google import genai
from google.genai import errors
from google.genai.types import GenerateContentConfig, GenerateContentResponse
from loguru import logger
from pydantic import BaseModel
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.core.ai.helpers import format_prompt, get_token_usage_metadata
from src.core.ai.prompts import JOB_DESC_W_CV_PROMPT, SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT
from src.core.config import settings
from src.core.cv_builders.comparison_cv_builder import ComparisonCVBuilder
from src.core.models.input_cv_fields import CVBody
from src.core.models.job_description_fields import JobDescriptionFields
from src.core.models.revised_cv_fields import (
    LLMResponse,
    RevisedCVResponseSchema,
)
from src.core.templates.renderers.llm import TemplateLLMRenderer
from src.core.utils.exceptions import ResponseParsingError


class CVTailorServiceConfig(BaseModel):
    model_name: str = settings.MODEL_NAME
    max_output_tokens: int = 2048
    retry_attempts: int = 3
    retry_min_wait: int = 4
    retry_max_wait: int = 10


class CVTailorService:
    retriable_errors: Tuple[Type[BaseException], ...] = (
        errors.ServerError,
        ResponseParsingError,
    )
    config: CVTailorServiceConfig = CVTailorServiceConfig()

    def __init__(self):
        self.client: genai.Client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.template_renderer: TemplateLLMRenderer = TemplateLLMRenderer()
        self.comparison_cv_builder: ComparisonCVBuilder = ComparisonCVBuilder()
        self.ai_suggestions_with_error = RevisedCVResponseSchema(
            explanations="ERROR: An error occurred. Please try again later.",
            suggestions="ERROR: An error occurred. Please try again later.",
            revised_professional_title=None,
            revised_professional_summary=None,
            revised_work_experience=None,
            revised_projects=None,
            revised_awards=None,
            revised_publications=None,
            revised_skills=None,
        )

    def _get_suggest_improvements_config(self) -> GenerateContentConfig:
        suggestion_config = GenerateContentConfig(
            max_output_tokens=self.config.max_output_tokens,
            system_instruction=SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=RevisedCVResponseSchema,
        )
        return suggestion_config

    @retry(
        reraise=True,
        retry=retry_if_exception_type(retriable_errors),
        stop=stop_after_attempt(config.retry_attempts),
        wait=wait_exponential(
            multiplier=1, min=config.retry_min_wait, max=config.retry_max_wait
        ),
    )
    async def get_cv_improvements(self, job_description: str, cv: str) -> LLMResponse:
        response: GenerateContentResponse
        prompt: str = format_prompt(
            JOB_DESC_W_CV_PROMPT, job_description=job_description, cv=cv
        )
        suggestion_config: GenerateContentConfig = (
            self._get_suggest_improvements_config()
        )

        try:
            logger.debug("Generating CV improvements...")
            response = await self.client.aio.models.generate_content(
                model=self.config.model_name,
                contents=prompt,
                config=suggestion_config,
            )
            logger.success("Successfully generated CV improvements.")
        except errors.APIError as e:
            logger.error(f"Google API error during CV improvements: {e}")
            raise

        if not response.parsed or response.parsed is None:
            logger.error("LLM response could not be parsed or was empty.")
            logger.info(f"LLM response: {response}")
            raise ResponseParsingError("LLM response could not be parsed or was empty.")

        metadata = get_token_usage_metadata(response)
        return LLMResponse(response=response, metadata=metadata)

    async def tailor_cv(
        self, original_cv: CVBody, job_description: JobDescriptionFields
    ):
        cv_string: str = self.template_renderer.cv_to_llm_format(original_cv)
        job_description_string: str = (
            self.template_renderer.job_description_to_llm_format(job_description)
        )

        try:
            llm_data: LLMResponse = await self.get_cv_improvements(
                job_description_string, cv_string
            )
            if llm_data.response is None or not hasattr(llm_data.response, "parsed"):
                raise ResponseParsingError(
                    "LLM response could not be parsed or was empty."
                )
            ai_suggestions: RevisedCVResponseSchema = llm_data.response.parsed
        except ResponseParsingError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return self.comparison_cv_builder.create_comparison_cv(
                original_cv, self.ai_suggestions_with_error
            )
        except Exception as e:
            logger.error(
                f"Unexpected error during get_cv_improvements: {e}", exc_info=True
            )
            raise

        return self.comparison_cv_builder.create_comparison_cv(
            original_cv, ai_suggestions
        )


cv_tailor_service = CVTailorService()
