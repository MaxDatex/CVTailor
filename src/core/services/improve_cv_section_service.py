from enum import Enum

from google.genai.types import GenerateContentConfig
from loguru import logger

from src.core.ai.helpers import format_prompt, get_token_usage_metadata
from src.core.ai.prompts import CV_SECTION_PROMPT, REWRITE_CV_SECTION_SYSTEM_PROMPT
from src.core.services.base_service import BaseAIService, BaseServiceConfig


class Instruction(str, Enum):
    CONCISE = "Concise"
    DETAILED = "Detailed"
    PROFESSIONAL = "Professional"
    INFORMAL = "Informal"


class ImproveCVSectionServiceConfig(BaseServiceConfig):
    max_output_tokens: int = 512


class ImproveCVSectionService(BaseAIService):
    def __init__(self):
        super().__init__(ImproveCVSectionServiceConfig())

    def _get_cv_section_improvements_config(self) -> GenerateContentConfig:
        suggestion_config = GenerateContentConfig(
            max_output_tokens=self.config.max_output_tokens,
            system_instruction=REWRITE_CV_SECTION_SYSTEM_PROMPT,
        )
        logger.info(f"Suggestion config: generated")
        return suggestion_config

    async def get_cv_section_improvements(
        self, cv_section: str, instruction: Instruction
    ) -> str:
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        async def _get_improvements():
            prompt: str = format_prompt(
                CV_SECTION_PROMPT, text=cv_section, instruction=instruction.value
            )
            suggestion_config = self._get_cv_section_improvements_config()

            logger.info("Prompt: generated")

            response = await self._make_api_call(
                prompt, suggestion_config, "CV section improvements"
            )

            metadata = get_token_usage_metadata(response)
            logger.info(f"Metadata: {metadata}")

            return self._extract_text_response(response)

        return await _get_improvements()


improve_cv_section_service = ImproveCVSectionService()
