from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
import os
from ai.prompts import SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT, JOB_DESC_W_CV_PROMPT
from models.revised_cv_fields import TestResponseSchema


load_dotenv()


def get_client(max_output_tokens=None):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    config = GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        system_instruction=SUGGEST_IMPROVEMENTS_SYSTEM_PROMPT,
        response_mime_type='application/json',
        response_schema=TestResponseSchema,
    )
    return client, config


def get_cv_improvements(job_description, cv, max_output_tokens=None):
    client, config = get_client(max_output_tokens)

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=JOB_DESC_W_CV_PROMPT.format(job_description=job_description, cv=cv),
        config=config,
    )

    return response
