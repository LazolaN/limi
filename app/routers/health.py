from fastapi import APIRouter

from app.db.engine import engine

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check with DB connectivity status."""
    status = {
        "status": "healthy",
        "service": "limi",
        "version": "0.2.0",
        "database": "connected" if engine is not None else "not_configured",
    }

    if engine is not None:
        try:
            async with engine.connect() as conn:
                await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
            status["database"] = "connected"
        except Exception:
            status["database"] = "unreachable"

    return status
