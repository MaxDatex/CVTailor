from typing import Tuple, Type

from google.genai import errors
from google.genai.types import GenerateContentConfig
from loguru import logger

from src.core.ai.helpers import format_prompt, get_token_usage_metadata
from src.core.ai.prompts import JOB_DESC_W_CV_PROMPT, SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT
from src.core.cv_builders.comparison_cv_builder import ComparisonCVBuilder
from src.core.models.input_cv_fields import CVBody
from src.core.models.job_description_fields import JobDescriptionFields
from src.core.models.revised_cv_fields import (
    LLMResponse,
    RevisedCVResponseSchema,
)
from src.core.services.base_service import BaseAIService, BaseServiceConfig
from src.core.utils.exceptions import ResponseParsingError


class CVTailorServiceConfig(BaseServiceConfig):
    max_output_tokens: int = 2048


class CVTailorService(BaseAIService):
    retriable_errors: Tuple[Type[BaseException], ...] = (
        errors.ServerError,
        ResponseParsingError,
    )

    def __init__(self):
        super().__init__(CVTailorServiceConfig())
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
        return GenerateContentConfig(
            max_output_tokens=self.config.max_output_tokens,
            system_instruction=SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=RevisedCVResponseSchema,
        )

    async def get_cv_improvements(self, job_description: str, cv: str) -> LLMResponse:
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        async def _get_improvements():
            prompt: str = format_prompt(
                JOB_DESC_W_CV_PROMPT, job_description=job_description, cv=cv
            )
            suggestion_config = self._get_suggest_improvements_config()
            response = await self._make_api_call(
                prompt, suggestion_config, "CV improvements"
            )

            if not response.parsed or response.parsed is None:
                logger.error("LLM response could not be parsed or was empty.")
                logger.info(f"LLM response: {response}")
                raise ResponseParsingError(
                    "LLM response could not be parsed or was empty."
                )

            metadata = get_token_usage_metadata(response)
            return LLMResponse(response=response, metadata=metadata)

        return await _get_improvements()

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
