from pydantic_settings import BaseSettings
from typing import Union

class Settings(BaseSettings):
    GOOGLE_API_KEY: Union[str, None] = None
    MAX_OUTPUT_TOKENS: Union[int, None] = 2048
    MODEL_NAME: str = "gemini-2.0-flash"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
