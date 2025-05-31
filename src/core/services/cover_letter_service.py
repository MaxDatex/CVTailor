from google.genai.types import GenerateContentConfig
from loguru import logger

from src.core.ai.helpers import format_prompt, get_token_usage_metadata
from src.core.ai.prompts import (
    GENERATE_COVER_LETTER_SYSTEM_PROMPT,
    JOB_DESC_W_CV_PROMPT,
)
from src.core.models.input_cv_fields import CVBody
from src.core.models.job_description_fields import JobDescriptionFields
from src.core.services.base_service import BaseAIService, BaseServiceConfig


class GenerateCoverLetterServiceConfig(BaseServiceConfig):
    max_output_tokens: int = 1024


class GenerateCoverLetterService(BaseAIService):
    def __init__(self):
        super().__init__(GenerateCoverLetterServiceConfig())

    def _get_cover_letter_config(self) -> GenerateContentConfig:
        suggestion_config = GenerateContentConfig(
            max_output_tokens=self.config.max_output_tokens,
            system_instruction=GENERATE_COVER_LETTER_SYSTEM_PROMPT,
        )
        logger.info(f"Suggestion config: generated")
        return suggestion_config

    async def generate_cover_letter(
        self, cv: CVBody, job_description: JobDescriptionFields
    ) -> str:
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        async def _generate_letter():
            cv_string: str = self.template_renderer.cv_to_llm_format(cv)
            job_description_string: str = (
                self.template_renderer.job_description_to_llm_format(job_description)
            )
            prompt: str = format_prompt(
                JOB_DESC_W_CV_PROMPT,
                cv=cv_string,
                job_description=job_description_string,
            )
            cover_letter_config = self._get_cover_letter_config()

            response = await self._make_api_call(
                prompt, cover_letter_config, "cover letter"
            )

            metadata = get_token_usage_metadata(response)
            logger.info(f"Metadata: {metadata}")

            return self._extract_text_response(response)

        return await _generate_letter()


cover_letter_service = GenerateCoverLetterService()
