from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai.types import GenerateContentConfig, GenerateContentResponse
import os
from ai.prompts import SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT, JOB_DESC_W_CV_PROMPT
from models.revised_cv_fields import TestResponseSchema
from models.input_cv_fields import CVBody
from models.job_description_fields import JobDescriptionFields
from typing import Tuple, Union
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from config import settings


load_dotenv()


def get_client(
    max_output_tokens: Union[int, None] = None,
) -> Tuple[genai.Client, GenerateContentConfig]:
    client: genai.Client
    config: GenerateContentConfig
    api_key: str = os.getenv("GOOGLE_API_KEY")
    logger.debug("Getting Google API key from environment variable...")
    if not api_key:
        logger.error("No API key found. Please set the GOOGLE_API_KEY environment variable.")
        raise ValueError("No API key found. Please set the GOOGLE_API_KEY environment variable.")

    client = genai.Client(api_key=api_key)
    config = GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        system_instruction=SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=TestResponseSchema,
    )
    return client, config


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_cv_improvements(
    job_description: JobDescriptionFields, cv: CVBody, max_output_tokens: Union[int, None] = None
) -> Union[GenerateContentResponse, None]:
    client: genai.Client
    config: GenerateContentConfig
    response: Union[GenerateContentResponse, None]

    client, config = get_client(max_output_tokens)
    logger.success("Successfully created Google API client.")
    try:
        logger.info("Generating CV improvements...")
        response = client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=JOB_DESC_W_CV_PROMPT.format(
                job_description=job_description, cv=cv
            ),
            config=config,
        )
    except errors.APIError as e:
        logger.error(
            f"An error occurred:\nError code: {e.code}\nError message: {e.message}\nError details: {e.details}"
        )
        response = None
    return response
