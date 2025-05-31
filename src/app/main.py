import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger as loguru_logger

from src.app.api.v1.endpoints import cover_letter, improve_section, tailor_cv
from src.core.config import settings  # Access settings for configuration

loguru_logger.level("INFO")

# Configure basic logging (you might want a more advanced setup for production)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description="FastAPI application interacting with Google Gemini API",
        debug=settings.ENVIRONMENT == "development",
    )

    # CORS middleware setup (adjust origins as needed for your frontend)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(tailor_cv.router, prefix="/api/v1", tags=["tailor_cv"])
    app.include_router(
        improve_section.router, prefix="/api/v1", tags=["improve_section"]
    )
    app.include_router(cover_letter.router, prefix="/api/v1", tags=["cover_letter"])
    return app


app = create_app()

# This is the entry point for Uvicorn
# To run: uvicorn app.main:app --reload
