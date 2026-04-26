from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Anthropic / LLM
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MONTHLY_BUDGET_USD: float = 30.0
    CLAUDE_MODEL: str = "claude-sonnet-4-6"
    CLAUDE_MODEL_HAIKU: str = "claude-haiku-4-5-20251001"
    CLAUDE_MODEL_SONNET: str = "claude-sonnet-4-6"
    CLAUDE_MODEL_OPUS: str = "claude-opus-4-7"
    CLAUDE_MAX_TOKENS: int = 1024

    # Cache (Redis)
    REDIS_CACHE_ENABLED: bool = False
    REDIS_CACHE_DEFAULT_TTL: int = 3600
    REDIS_URL: str = "redis://localhost:6379"

    # Knowledge (RAG — Weaviate placeholder)
    WEAVIATE_URL: str = "http://localhost:8080"

    # Environment / logging
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = ""
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # WhatsApp Cloud API (Meta) — see docs/meta-whatsapp-setup.md
    WHATSAPP_VERIFY_TOKEN: str = ""
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_APP_SECRET: str = ""
    WHATSAPP_API_BASE_URL: str = "https://graph.facebook.com/v21.0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
