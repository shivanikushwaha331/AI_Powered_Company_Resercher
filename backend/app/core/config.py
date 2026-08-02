"""
Application Configuration Module using Pydantic Settings.
Manages environment variables and application runtime parameters.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Settings definition."""

    # Application details
    APP_NAME: str = "AI Company Research Assistant"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # External LLM Keys
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gemini-2.5-flash"

    # Search Engine Keys
    TAVILY_API_KEY: str = ""
    SERPER_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


# Global settings instance
settings = Settings()
