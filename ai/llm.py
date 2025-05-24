from typing import Union, Dict, Optional

import tenacity
from google import genai
from google.genai import errors
from google.genai.types import GenerateContentConfig, GenerateContentResponse
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_not_exception_type

from ai.prompts import JOB_DESC_W_CV_PROMPT, SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT
from config import settings
from models.revised_cv_fields import RevisedCVResponseSchema, LLMResponse
from utils.exceptions import ResponseParsingError, ClientInitializationError, MissingAPIKeyError


_CLIENT: Optional[genai.Client] = None
_IS_INITIALIZED: bool = False
_TESTING: bool = True


@retry(
    retry=retry_if_not_exception_type((errors.ClientError, MissingAPIKeyError)),
    stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=1, min=settings.RETRY_MIN_WAIT, max=settings.RETRY_MAX_WAIT
    ),
)
def _init_ai_resources() -> None:
    global _CLIENT, _IS_INITIALIZED
    if _IS_INITIALIZED:
        logger.debug("AI resources already initialized.")
        return None

    api_key: Optional[str] = settings.GOOGLE_API_KEY
    no_key_error_msg: str = "No API key found. Please set the GOOGLE_API_KEY environment variable."

    logger.debug("Getting Google API key from environment variable...")
    if not api_key:
        logger.error(no_key_error_msg)
        raise MissingAPIKeyError(no_key_error_msg)

    # try:
    _CLIENT = genai.Client(api_key=api_key)
    # Checking for API key correctness
    _CLIENT.models.list()
    _IS_INITIALIZED = True
    logger.success("Successfully initialized Google API client and model.")
    # except errors.ClientError as e:
    #     logger.error(f"Failed to initialize AI resources: {e.cod}: {e.message}")
    #     raise InvalidAPIKeyError(f"Failed to initialize AI resources: {e}") from e
    # except Exception as e:
    #     logger.error(f"Failed to initialize AI resources: {e}")
    #     raise InvalidAPIKeyError(f"Failed to initialize AI resources: {e}") from e
    return None


def get_suggest_improvements_config(max_output_tokens: Optional[int] = None) -> GenerateContentConfig:
    config = GenerateContentConfig(
        max_output_tokens=max_output_tokens,
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
    # retry=retry_if_not_exception_type(MissingAPIKeyError),
    stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=1, min=settings.RETRY_MIN_WAIT, max=settings.RETRY_MAX_WAIT
    ),
)
def get_cv_improvements(job_description: str, cv: str) -> LLMResponse:
    client: genai.Client
    config: GenerateContentConfig
    response: GenerateContentResponse
    success: bool

    global _CLIENT, _IS_INITIALIZED
    config = get_suggest_improvements_config()

    if not _IS_INITIALIZED or _CLIENT is None:
        logger.error("AI resources were not initialized. Attempting to initialize now.")
        try:
            _init_ai_resources()
        except tenacity.RetryError as e:
            logger.error(f"Failed to initialize AI resources: {e}")
            raise ClientInitializationError(e) from e
        # if not _IS_INITIALIZED or _CLIENT is None:
            # return LLMResponse(success=False, response=None, metadata=None, error="AI resources failed to initialize.")

    # try:
    logger.debug("Generating CV improvements...")

    response = _CLIENT.models.generate_content(
        model=settings.MODEL_NAME,
        contents=JOB_DESC_W_CV_PROMPT.format(
            job_description=job_description, cv=cv
        ),
        config=config,
    )
    logger.success("Successfully generated CV improvements.")

    if response.parsed is None or not response.parsed:
        logger.error("LLM response could not be parsed or was empty.")
        raise ResponseParsingError("LLM response could not be parsed or was empty.")

    metadata = get_token_usage_metadata(response)
    return LLMResponse(
        success=True, response=response, metadata=metadata, error=None
    )
    # except ResponseParsingError:
    #     logger.error("LLM response could not be parsed or was empty.")
    #     return LLMResponse(
    #         success=False, response=None, metadata=None, error="Response parsing error."
    #     )
    # except errors.APIError as e:
    #     logger.error(
    #         f"An error occurred:\nError code: {e.code}\nError message: {e.message}\nError details: {e.details}"
    #     )
    #     return LLMResponse(success=False, response=None, metadata=None, error=e.message)
    # except MissingAPIKeyError as e:
    #     logger.error(str(e))
    #     return LLMResponse(success=False, response=None, metadata=None, error=str(e))
    # except Exception as e:
    #     logger.error(f"An unexpected error occurred: {e.with_traceback()}")
    #     return LLMResponse(success=False, response=None, metadata=None, error=str(e))
