from typing import Any, Dict, Optional

from google.genai.types import GenerateContentResponse
from loguru import logger


def get_token_usage_metadata(
    response: GenerateContentResponse,
) -> Dict[str, Optional[int]]:
    metadata: Dict[str, Optional[int]] = {
        "input_tokens_count": None,
        "output_tokens_count": None,
    }
    if not response.usage_metadata:
        logger.warning("No usage metadata found in the response.")
        return metadata

    metadata["input_tokens_count"] = response.usage_metadata.prompt_token_count
    metadata["output_tokens_count"] = response.usage_metadata.candidates_token_count
    return metadata


def format_prompt(prompt: str, **inputs: Any) -> str:
    return prompt.format(**inputs)
