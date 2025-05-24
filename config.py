from typing import Optional
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    MAX_OUTPUT_TOKENS: Optional[int] = 2048
    MODEL_NAME: str = "gemini-2.0-flash"
    RETRY_ATTEMPTS: int = 3
    RETRY_MIN_WAIT: int = 4
    RETRY_MAX_WAIT: int = 10
    ENVIRONMENT: str = "development"

    class Config:
        env_file = "../.env"


settings = Settings()
