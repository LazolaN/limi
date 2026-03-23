import logging

from fastapi import FastAPI

from app.config import settings
from app.routers import query, whatsapp, health

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

app = FastAPI(
    title="InDaba API",
    description="AI Agricultural Advisory Agent for South African Farmers",
    version="0.1.0",
)

app.include_router(health.router, tags=["health"])
app.include_router(query.router, prefix="/api", tags=["advisory"])
app.include_router(whatsapp.router, prefix="/webhook", tags=["webhooks"])
