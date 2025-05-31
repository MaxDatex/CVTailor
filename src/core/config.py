import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    MAX_OUTPUT_TOKENS: int = 2048
    MODEL_NAME: str = "gemini-2.0-flash"

    APP_NAME: str = "My FastAPI GenAI App"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings():
    return Settings()


settings = get_settings()
