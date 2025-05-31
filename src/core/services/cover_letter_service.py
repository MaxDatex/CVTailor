from typing import Tuple, Type

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
from src.core.ai.prompts import (
    GENERATE_COVER_LETTER_SYSTEM_PROMPT,
    JOB_DESC_W_CV_PROMPT,
)
from src.core.config import settings
from src.core.models.input_cv_fields import CVBody
from src.core.models.job_description_fields import JobDescriptionFields
from src.core.templates.renderers.llm import TemplateLLMRenderer


class GenerateCoverLetterServiceConfig(BaseModel):
    model_name: str = settings.MODEL_NAME
    max_output_tokens: int = 512
    retry_attempts: int = 3
    retry_min_wait: int = 4
    retry_max_wait: int = 10


class GenerateCoverLetterService:
    retriable_errors: Tuple[Type[BaseException]] = (errors.ServerError,)
    config: GenerateCoverLetterServiceConfig = GenerateCoverLetterServiceConfig()

    def __init__(self):
        self.client: genai.Client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.template_renderer: TemplateLLMRenderer = TemplateLLMRenderer()

    def _get_cover_letter_config(self) -> GenerateContentConfig:
        suggestion_config = GenerateContentConfig(
            max_output_tokens=self.config.max_output_tokens,
            system_instruction=GENERATE_COVER_LETTER_SYSTEM_PROMPT,
        )
        logger.info(f"Suggestion config: generated")
        return suggestion_config

    @retry(
        reraise=True,
        retry=retry_if_exception_type(retriable_errors),
        stop=stop_after_attempt(config.retry_attempts),
        wait=wait_exponential(
            multiplier=1, min=config.retry_min_wait, max=config.retry_max_wait
        ),
    )
    async def generate_cover_letter(
        self, cv: CVBody, job_description: JobDescriptionFields
    ) -> str:
        response: GenerateContentResponse
        cv_string: str = self.template_renderer.cv_to_llm_format(cv)
        job_description_string: str = (
            self.template_renderer.job_description_to_llm_format(job_description)
        )
        prompt: str = format_prompt(
            JOB_DESC_W_CV_PROMPT, cv=cv_string, job_description=job_description_string
        )
        cover_letter_config: GenerateContentConfig = self._get_cover_letter_config()

        try:
            logger.debug("Generating cover letter...")
            response = await self.client.aio.models.generate_content(
                model=self.config.model_name,
                contents=prompt,
                config=cover_letter_config,
            )

            logger.success("Successfully generated cover letter.")
        except errors.APIError as e:
            logger.error(f"Google API error during CV improvements: {e}")
            raise
        metadata = get_token_usage_metadata(response)
        logger.info(f"Metadata: {metadata}")
        if (
            response.candidates is None
            or not response.candidates
            or not response.candidates[0].content
            or not response.candidates[0].content.parts
        ):
            logger.error("LLM response could not be parsed or was empty.")
            logger.info(f"LLM response: {response}")
            raise ValueError("LLM response could not be parsed or was empty.")
        return response.candidates[0].content.parts[0].text


cover_letter_service = GenerateCoverLetterService()
