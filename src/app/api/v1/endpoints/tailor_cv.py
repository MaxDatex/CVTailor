from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.app.dependencies.common import get_cv_tailor_service
from src.core.models.comparison_cv_fields import ComparisonCV
from src.core.models.input_cv_fields import CVBody
from src.core.models.job_description_fields import JobDescriptionFields
from src.core.services.cv_tailor_service import CVTailorService

router = APIRouter()


class ChatRequest(BaseModel):
    cv: CVBody
    job_description: JobDescriptionFields


class ChatResponse(BaseModel):
    response: ComparisonCV


@router.post("/tailor_cv", response_model=ChatResponse)
async def chat_with_gemini(
    request: ChatRequest,
    cv_tailor_service: CVTailorService = Depends(get_cv_tailor_service),
):
    try:
        generated_text = await cv_tailor_service.tailor_cv(
            request.cv, request.job_description
        )
        return ChatResponse(response=generated_text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interacting with Gemini API: {e}",
        )
