import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.db.engine import dispose_engine
from app.routers import query, whatsapp, health, financial, analytics

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


def _validate_env() -> None:
    """Fail fast in production if required secrets are missing or default."""
    if settings.ENVIRONMENT != "production":
        return
    required = {
        "ANTHROPIC_API_KEY": settings.ANTHROPIC_API_KEY,
        "DATABASE_URL": settings.DATABASE_URL,
        "WHATSAPP_PHONE_NUMBER_ID": settings.WHATSAPP_PHONE_NUMBER_ID,
        "WHATSAPP_ACCESS_TOKEN": settings.WHATSAPP_ACCESS_TOKEN,
        "WHATSAPP_APP_SECRET": settings.WHATSAPP_APP_SECRET,
        "WHATSAPP_VERIFY_TOKEN": settings.WHATSAPP_VERIFY_TOKEN,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeError(
            f"Missing required env vars in production: {', '.join(missing)}"
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    _validate_env()
    yield
    from app.services.whatsapp_sender import close_client as close_whatsapp_client
    await close_whatsapp_client()
    await dispose_engine()


app = FastAPI(
    title="Limi API",
    description="AI Agricultural Advisory & Embedded Finance for South African Farmers",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(health.router, tags=["health"])
app.include_router(query.router, prefix="/api", tags=["advisory"])
app.include_router(whatsapp.router, prefix="/webhook", tags=["webhooks"])
app.include_router(financial.router, prefix="/api/financial", tags=["financial"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
