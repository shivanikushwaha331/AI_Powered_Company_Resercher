"""
Application Configuration Module using Pydantic Settings.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application runtime parameters and environment variables."""

    # Application Info
    APP_NAME: str = "AI Company Research Assistant"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Host & Port
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Mock Mode Flag
    MOCK_MODE: bool = True

    # External API Keys
    OPENROUTER_API_KEY: str = ""
    SERPER_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    TAVILY_API_KEY: str = ""

    # OpenRouter Models
    DEFAULT_OPENROUTER_MODEL: str = "google/gemini-2.5-flash"
    AVAILABLE_OPENROUTER_MODELS: List[str] = [
        "google/gemini-2.5-flash",
        "anthropic/claude-3.5-sonnet",
        "openai/gpt-4o-mini",
        "deepseek/deepseek-r1",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
