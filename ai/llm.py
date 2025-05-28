from typing import Dict, Optional, Union

from google import genai
from google.genai import errors
from google.genai.types import GenerateContentConfig, GenerateContentResponse
from loguru import logger
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from ai.prompts import JOB_DESC_W_CV_PROMPT, SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT
from config import settings
from models.revised_cv_fields import LLMResponse, RevisedCVResponseSchema
from utils.exceptions import (ClientInitializationError, MissingAPIKeyError,
                              ResponseParsingError)

_CLIENT: Optional[genai.Client] = None
_IS_INITIALIZED: bool = False


def _init_ai_resources() -> None:
    global _CLIENT, _IS_INITIALIZED
    if _IS_INITIALIZED:
        logger.debug("AI resources already initialized.")
        return None

    api_key: Optional[str] = settings.GOOGLE_API_KEY
    no_key_error_msg: str = (
        "No API key found. Please set the GOOGLE_API_KEY environment variable."
    )

    logger.debug("Getting Google API key from environment variable...")
    if not api_key:
        logger.error(no_key_error_msg)
        raise MissingAPIKeyError(no_key_error_msg)

    _CLIENT = genai.Client(api_key=api_key)
    # Checking for API key correctness
    _CLIENT.models.list()
    _IS_INITIALIZED = True
    logger.success("Successfully initialized Google API client and model.")

    return None


retriable_errors = (errors.ServerError,)


def get_suggest_improvements_config() -> GenerateContentConfig:
    config = GenerateContentConfig(
        max_output_tokens=settings.MAX_OUTPUT_TOKENS,
        system_instruction=SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=RevisedCVResponseSchema,
    )
    return config


def get_token_usage_metadata(response: GenerateContentResponse) -> Dict:
    metadata: Dict[str, Union[int, None]] = {
        "input_tokens_count": None,
        "output_tokens_count": None,
    }
    if not response.usage_metadata:
        logger.warning("No usage metadata found in the response.")
        return metadata

    metadata["input_tokens_count"] = response.usage_metadata.prompt_token_count
    metadata["output_tokens_count"] = response.usage_metadata.candidates_token_count
    return metadata


@retry(
    reraise=True,
    retry=retry_if_exception_type(retriable_errors),
    stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=1, min=settings.RETRY_MIN_WAIT, max=settings.RETRY_MAX_WAIT
    ),
)
def get_cv_improvements(job_description: str, cv: str) -> LLMResponse:
    client: genai.Client
    config: GenerateContentConfig
    response: GenerateContentResponse

    global _CLIENT, _IS_INITIALIZED
    config = get_suggest_improvements_config()

    if not _IS_INITIALIZED or _CLIENT is None:
        logger.error("AI resources were not initialized. Attempting to initialize now.")
        try:
            _init_ai_resources()
        except Exception as e:
            logger.error(f"Failed to initialize AI resources: {str(e)}")
            raise ClientInitializationError(e) from e

    logger.debug("Generating CV improvements...")

    response = _CLIENT.models.generate_content(
        model=settings.MODEL_NAME,
        contents=JOB_DESC_W_CV_PROMPT.format(job_description=job_description, cv=cv),
        config=config,
    )
    logger.success("Successfully generated CV improvements.")

    if response.parsed is None or not response.parsed:
        logger.error("LLM response could not be parsed or was empty.")
        raise ResponseParsingError("LLM response could not be parsed or was empty.")

    metadata = get_token_usage_metadata(response)
    return LLMResponse(response=response, metadata=metadata)
