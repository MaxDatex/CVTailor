import os
from typing import Tuple, Union, Dict

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai.types import GenerateContentConfig, GenerateContentResponse
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from ai.prompts import JOB_DESC_W_CV_PROMPT, SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT
from config import settings
from models.revised_cv_fields import RevisedCVResponseSchema, LLMResponse
from utils.exceptions import ResponseParsingError


load_dotenv()


def get_client(
    max_output_tokens: Union[int, None] = None,
) -> Tuple[genai.Client, GenerateContentConfig]:
    client: genai.Client
    config: GenerateContentConfig
    api_key: Union[str, None] = os.getenv("GOOGLE_API_KEY")
    logger.debug("Getting Google API key from environment variable...")
    if not api_key:
        logger.error(
            "No API key found. Please set the GOOGLE_API_KEY environment variable."
        )
        raise ValueError(
            "No API key found. Please set the GOOGLE_API_KEY environment variable."
        )

    client = genai.Client(api_key=api_key)
    config = GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        system_instruction=SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=RevisedCVResponseSchema,
    )
    return client, config


@retry(
    stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=1, min=settings.RETRY_MIN_WAIT, max=settings.RETRY_MAX_WAIT
    ),
)
def get_cv_improvements(
    job_description: str,
    cv: str,
    max_output_tokens: Union[int, None] = None,
) -> LLMResponse:
    client: genai.Client
    config: GenerateContentConfig
    response: GenerateContentResponse
    success: bool

    client, config = get_client(max_output_tokens)
    logger.success("Successfully created Google API client.")
    try:
        logger.debug("Generating CV improvements...")
        response = client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=JOB_DESC_W_CV_PROMPT.format(
                job_description=job_description, cv=cv
            ),
            config=config,
        )
        logger.success("Successfully generated CV improvements.")
        if response.parsed is None or not response.parsed:
            raise ResponseParsingError()

        metadata: Dict[str, Union[int, None]] = {
            "input_tokens_count": None,
            "output_tokens_count": None,
        }
        if not response.usage_metadata:
            logger.warning("No usage metadata found in the response.")
            return LLMResponse(
                success=True, response=response, metadata=metadata, error=None
            )
        metadata["input_tokens_count"] = response.usage_metadata.candidates_token_count
        metadata["output_tokens_count"] = response.usage_metadata.prompt_token_count
        return LLMResponse(
            success=True, response=response, metadata=metadata, error=None
        )
    except ResponseParsingError:
        logger.error("LLM response could not be parsed or was empty.")
        return LLMResponse(
            success=False, response=None, metadata=None, error="Response parsing error."
        )
    except errors.APIError as e:
        logger.error(
            f"An error occurred:\nError code: {e.code}\nError message: {e.message}\nError details: {e.details}"
        )
        return LLMResponse(success=False, response=None, metadata=None, error=e.message)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return LLMResponse(success=False, response=None, metadata=None, error=str(e))
