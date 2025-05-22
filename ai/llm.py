from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai.types import GenerateContentConfig, GenerateContentResponse
import os
from ai.prompts import SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT, JOB_DESC_W_CV_PROMPT
from models.revised_cv_fields import TestResponseSchema
from typing import Tuple, Union


load_dotenv()


def get_client(
    max_output_tokens: Union[int, None] = None,
) -> Tuple[genai.Client, GenerateContentConfig]:
    client: genai.Client
    config: GenerateContentConfig

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    config = GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        system_instruction=SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=TestResponseSchema,
    )
    return client, config


def get_cv_improvements(
    job_description: str, cv: str, max_output_tokens: Union[int, None] = None
) -> Union[GenerateContentResponse, None]:
    client: genai.Client
    config: GenerateContentConfig
    response: Union[GenerateContentResponse, None]

    client, config = get_client(max_output_tokens)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=JOB_DESC_W_CV_PROMPT.format(
                job_description=job_description, cv=cv
            ),
            config=config,
        )
    except errors.APIError as e:
        print(
            f"An error occurred:\nError code: {e.code}\nError message: {e.message}\nError details: {e.details}"
        )
        response = None
    return response
