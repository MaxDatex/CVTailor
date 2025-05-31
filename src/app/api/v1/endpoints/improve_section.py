from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator

from src.app.dependencies.common import get_improve_cv_section_service
from src.core.services.improve_cv_section_service import (
    ImproveCVSectionService,
    Instruction,
)

router = APIRouter()


class CVSectionChatRequest(BaseModel):
    cv_section: str
    instruction: Instruction

    @field_validator("cv_section")
    @classmethod
    def validate_cv_section_length(cls, cv_section: str) -> str:
        if len(cv_section) > 100:
            raise ValueError(f"CV section too long: (max: 100 chars)")
        return cv_section


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
            request.cv_section, request.instruction
        )
        return CVSectionChatResponse(response=generated_text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interacting with Gemini API: {e}",
        )
