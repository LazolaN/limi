from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    CLAUDE_MAX_TOKENS: int = 1024
    REDIS_URL: str = "redis://localhost:6379"
    WEAVIATE_URL: str = "http://localhost:8080"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    WHATSAPP_VERIFY_TOKEN: str = "indaba-verify-token"
    WHATSAPP_API_TOKEN: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
