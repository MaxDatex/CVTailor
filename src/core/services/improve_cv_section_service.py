from enum import Enum
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
from src.core.ai.prompts import CV_SECTION_PROMPT, REWRITE_CV_SECTION_SYSTEM_PROMPT
from src.core.config import settings
from src.core.templates.renderers.llm import TemplateLLMRenderer


class Instruction(str, Enum):
    CONCISE = "Concise"
    DETAILED = "Detailed"
    PROFESSIONAL = "Professional"
    INFORMAL = "Informal"


class ImproveCVSectionServiceConfig(BaseModel):
    model_name: str = settings.MODEL_NAME
    max_output_tokens: int = 512
    retry_attempts: int = 3
    retry_min_wait: int = 4
    retry_max_wait: int = 10


class ImproveCVSectionService:
    retriable_errors: Tuple[Type[BaseException]] = (errors.ServerError,)
    config: ImproveCVSectionServiceConfig = ImproveCVSectionServiceConfig()

    def __init__(self):
        self.client: genai.Client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.template_renderer: TemplateLLMRenderer = TemplateLLMRenderer()

    def _get_cv_section_improvements_config(self) -> GenerateContentConfig:
        suggestion_config = GenerateContentConfig(
            max_output_tokens=self.config.max_output_tokens,
            system_instruction=REWRITE_CV_SECTION_SYSTEM_PROMPT,
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
    async def get_cv_section_improvements(
        self, cv_section: str, instruction: Instruction
    ) -> str:
        response: GenerateContentResponse
        prompt: str = format_prompt(
            CV_SECTION_PROMPT, text=cv_section, instruction=instruction.value
        )
        suggestion_config: GenerateContentConfig = (
            self._get_cv_section_improvements_config()
        )

        logger.info(f"Prompt: generated")

        try:
            logger.debug("Generating CV section improvements...")
            response = await self.client.aio.models.generate_content(
                model=self.config.model_name,
                contents=prompt,
                config=suggestion_config,
            )

            logger.success("Successfully generated CV section improvements.")
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


improve_cv_section_service = ImproveCVSectionService()
