import re
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


def postprocess_text_response(text_response: str) -> str:
    #  Remove Markdown headings '# Heading'
    text_response = re.sub(r"^[#]+\s*.*$", "", text_response, flags=re.MULTILINE)
    #  Remove **bold** and *italic* Markdown
    text_response = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text_response)  # For bold
    text_response = re.sub(r"(\*|_)(.*?)\1", r"\2", text_response)  # For italic
    #  Remove blockquotes '>'
    text_response = re.sub(r"^\s*>\s*", "", text_response, flags=re.MULTILINE)
    #  Remove lists '-' item, '*' item, '1.' item
    text_response = re.sub(r"^\s*[-*+]\s*", "", text_response, flags=re.MULTILINE)
    text_response = re.sub(r"^\s*\d+\.\s*", "", text_response, flags=re.MULTILINE)
    #  Remove horizontal rules (e.g., ---, ***, ___)
    text_response = re.sub(r"^\s*[-*_]{3,}\s*$", "", text_response, flags=re.MULTILINE)
    #  Remove links (e.g., [text](url)) - keep only the text
    text_response = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text_response)
    #  Remove images (e.g., ![alt text](url)) - remove entirely
    text_response = re.sub(r"!\[.*?\]\(.*?\)", "", text_response)
    #  Remove extra spaces around punctuation that might be left from Markdown removal
    text_response = re.sub(r"\s+([.,!?;:])", r"\1", text_response)
    text_response = text_response.replace("\\n", " ")
    text_response = text_response.replace("\\t", " ")
    text_response = text_response.replace("\n", " ")
    text_response = text_response.replace("\t", " ")
    text_response = text_response.replace("\r", " ")
    text_response = re.sub(r"\s+", " ", text_response).strip()
    return text_response
