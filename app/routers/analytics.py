import logging
from datetime import datetime, timedelta, UTC

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import get_session
from app.db.models import QueryLogDB
from app.services.token_tracker import estimate_cost

logger = logging.getLogger("limi.analytics")

router = APIRouter()


@router.get("/queries")
async def query_volume(
    days: int = Query(30, ge=1, le=365),
    session: AsyncSession | None = Depends(get_session),
):
    """Query volume over time, aggregated by day."""
    if session is None:
        return {"status": "no_database", "data": [], "message": "Connect PostgreSQL to enable analytics"}

    since = datetime.now(UTC) - timedelta(days=days)
    result = await session.execute(
        select(
            func.date_trunc("day", QueryLogDB.created_at).label("day"),
            func.count().label("count"),
        )
        .where(QueryLogDB.created_at >= since)
        .group_by(text("1"))
        .order_by(text("1"))
    )
    return {"status": "ok", "data": [{"day": str(row.day), "count": row.count} for row in result]}


@router.get("/intents")
async def intent_distribution(
    days: int = Query(30, ge=1, le=365),
    session: AsyncSession | None = Depends(get_session),
):
    """Intent distribution for the given period."""
    if session is None:
        return {"status": "no_database", "data": []}

    since = datetime.now(UTC) - timedelta(days=days)
    result = await session.execute(
        select(
            QueryLogDB.intent,
            func.count().label("count"),
        )
        .where(QueryLogDB.created_at >= since)
        .group_by(QueryLogDB.intent)
        .order_by(func.count().desc())
    )
    return {"status": "ok", "data": [{"intent": row.intent, "count": row.count} for row in result]}


@router.get("/escalation-rate")
async def escalation_rate(
    days: int = Query(30, ge=1, le=365),
    session: AsyncSession | None = Depends(get_session),
):
    """Escalation rate over time."""
    if session is None:
        return {"status": "no_database", "data": {}}

    since = datetime.now(UTC) - timedelta(days=days)
    result = await session.execute(
        select(
            func.count().label("total"),
            func.sum(func.cast(QueryLogDB.escalated, type_=__import__("sqlalchemy").Integer)).label("escalated"),
        )
        .where(QueryLogDB.created_at >= since)
    )
    row = result.one()
    total = row.total or 0
    escalated = row.escalated or 0
    rate = (escalated / total * 100) if total > 0 else 0

    return {
        "status": "ok",
        "data": {
            "total_queries": total,
            "escalated_queries": escalated,
            "escalation_rate_pct": round(rate, 2),
        },
    }


@router.get("/unit-economics")
async def unit_economics(
    days: int = Query(30, ge=1, le=365),
    session: AsyncSession | None = Depends(get_session),
):
    """Unit economics: cost per query, model distribution."""
    if session is None:
        return {
            "status": "no_database",
            "data": {
                "message": "Connect PostgreSQL to enable analytics",
                "estimated_cost_per_query_usd_cents": 1.5,
                "note": "Estimate based on average Sonnet 4 usage (3000 input + 1000 output tokens)",
            },
        }

    since = datetime.now(UTC) - timedelta(days=days)
    result = await session.execute(
        select(
            func.count().label("total_queries"),
            func.avg(QueryLogDB.cost_usd_cents).label("avg_cost"),
            func.sum(QueryLogDB.cost_usd_cents).label("total_cost"),
            func.avg(QueryLogDB.input_tokens).label("avg_input_tokens"),
            func.avg(QueryLogDB.output_tokens).label("avg_output_tokens"),
            func.avg(QueryLogDB.pipeline_duration_ms).label("avg_latency_ms"),
            func.sum(func.cast(QueryLogDB.cache_hit, type_=__import__("sqlalchemy").Integer)).label("cache_hits"),
        )
        .where(QueryLogDB.created_at >= since)
    )
    row = result.one()

    total = row.total_queries or 0
    cache_hits = row.cache_hits or 0
    cache_rate = (cache_hits / total * 100) if total > 0 else 0

    return {
        "status": "ok",
        "data": {
            "total_queries": total,
            "avg_cost_per_query_usd_cents": round(float(row.avg_cost or 0), 4),
            "total_cost_usd_cents": round(float(row.total_cost or 0), 2),
            "avg_input_tokens": round(float(row.avg_input_tokens or 0)),
            "avg_output_tokens": round(float(row.avg_output_tokens or 0)),
            "avg_latency_ms": round(float(row.avg_latency_ms or 0), 1),
            "cache_hit_rate_pct": round(cache_rate, 2),
        },
    }


@router.get("/funnel")
async def financial_funnel(
    session: AsyncSession | None = Depends(get_session),
):
    """Financial product conversion funnel (MVP: based on intent counts)."""
    if session is None:
        return {"status": "no_database", "data": {}}

    # Count financial intent queries as top of funnel
    financial_intents = ["loan_inquiry", "insurance_inquiry", "savings_inquiry", "market_linkage"]
    result = await session.execute(
        select(
            QueryLogDB.intent,
            func.count().label("count"),
        )
        .where(QueryLogDB.intent.in_(financial_intents))
        .group_by(QueryLogDB.intent)
    )

    intent_counts = {row.intent: row.count for row in result}

    return {
        "status": "ok",
        "data": {
            "financial_queries_total": sum(intent_counts.values()),
            "by_intent": intent_counts,
            "note": "Transaction tracking (applications, approvals, disbursements) requires DB integration",
        },
    }
