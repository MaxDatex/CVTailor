from src.core.config import Settings, get_settings
from src.core.services.cover_letter_service import cover_letter_service
from src.core.services.cv_tailor_service import cv_tailor_service
from src.core.services.improve_cv_section_service import improve_cv_section_service


def get_cv_tailor_service():
    """Dependency to provide the CVTailor service."""
    return cv_tailor_service


def get_improve_cv_section_service():
    """Dependency to provide the ImproveCVSection service."""
    return improve_cv_section_service


def get_generate_cover_letter_service():
    """Dependency to provide the GenerateCoverLetter service."""
    return cover_letter_service


def get_app_settings() -> Settings:
    """Dependency to provide application settings."""
    return get_settings()
