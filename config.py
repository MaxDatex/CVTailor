from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: Union[str, None] = None
    MAX_OUTPUT_TOKENS: Union[int, None] = 2048
    MODEL_NAME: str = "gemini-2.0-flash"
    RETRY_ATTEMPTS: int = 3
    RETRY_MIN_WAIT: int = 4
    RETRY_MAX_WAIT: int = 10
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
