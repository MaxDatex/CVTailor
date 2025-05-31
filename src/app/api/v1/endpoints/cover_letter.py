from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.app.dependencies.common import get_generate_cover_letter_service
from src.core.models.input_cv_fields import CVBody
from src.core.models.job_description_fields import JobDescriptionFields
from src.core.services.cover_letter_service import GenerateCoverLetterService

router = APIRouter()


class CoverLetterChatRequest(BaseModel):
    cv: CVBody
    job_description: JobDescriptionFields


class CoverLetterChatResponse(BaseModel):
    response: str


@router.post("/cover_letter", response_model=CoverLetterChatResponse)
async def chat_with_gemini(
    request: CoverLetterChatRequest,
    generate_cover_letter_service: GenerateCoverLetterService = Depends(
        get_generate_cover_letter_service
    ),
):
    try:
        generated_text = await generate_cover_letter_service.generate_cover_letter(
            request.cv, request.job_description
        )
        return CoverLetterChatResponse(response=generated_text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interacting with Gemini API: {e}",
        )
