from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.app.dependencies.common import get_improve_cv_section_service
from src.core.services.improve_cv_section_service import (
    ImproveCVSectionService,
    Instruction,
)

router = APIRouter()


class CVSectionChatRequest(BaseModel):
    text: str
    instruction: Instruction


class CVSectionChatResponse(BaseModel):
    response: str


@router.post("/improve_section", response_model=CVSectionChatResponse)
async def chat_with_gemini(
    request: CVSectionChatRequest,
    improve_cv_section_service: ImproveCVSectionService = Depends(
        get_improve_cv_section_service
    ),
):
    try:
        generated_text = await improve_cv_section_service.get_cv_section_improvements(
            request.text, request.instruction
        )
        return CVSectionChatResponse(response=generated_text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interacting with Gemini API: {e}",
        )
