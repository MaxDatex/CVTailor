from abc import ABC
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

from src.core.ai.helpers import postprocess_text_response
from src.core.config import settings
from src.core.templates.renderers.llm import TemplateLLMRenderer


class BaseServiceConfig(BaseModel):
    model_name: str = settings.MODEL_NAME
    max_output_tokens: int = 512
    retry_attempts: int = 3
    retry_min_wait: int = 4
    retry_max_wait: int = 10


class BaseAIService(ABC):
    retriable_errors: Tuple[Type[BaseException], ...] = (errors.ServerError,)

    def __init__(self, config: BaseServiceConfig):
        self.config = config
        logger.info(f"Loading client...")
        self.client: genai.Client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.template_renderer: TemplateLLMRenderer = TemplateLLMRenderer()

    def _create_retry_decorator(self):
        return retry(
            reraise=True,
            retry=retry_if_exception_type(self.retriable_errors),
            stop=stop_after_attempt(self.config.retry_attempts),
            wait=wait_exponential(
                multiplier=1,
                min=self.config.retry_min_wait,
                max=self.config.retry_max_wait,
            ),
        )

    def _extract_text_response(
        self,
        response: GenerateContentResponse,
        fallback_message: str = "Something unexpected happened. Please try again later.",
    ) -> str:
        if (
            response.candidates is None
            or not response.candidates
            or not response.candidates[0].content
            or not response.candidates[0].content.parts
        ):
            logger.error("LLM response could not be parsed or was empty.")
            logger.info(f"LLM response: {response}")
            raise ValueError("LLM response could not be parsed or was empty.")

        return (
            postprocess_text_response(response.candidates[0].content.parts[0].text)
            or fallback_message
        )

    async def _make_api_call(
        self, prompt: str, config: GenerateContentConfig, operation_name: str
    ) -> GenerateContentResponse:
        try:
            logger.debug(f"Generating {operation_name}...")
            response = await self.client.aio.models.generate_content(
                model=self.config.model_name,
                contents=prompt,
                config=config,
            )
            logger.success(f"Successfully generated {operation_name}.")
            return response
        except errors.APIError as e:
            logger.error(f"Google API error during {operation_name}: {e}")
            raise
