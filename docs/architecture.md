# Limi — Architecture

## Overview

Limi is an embedded agri-fintech platform serving South African farmers via WhatsApp, USSD, Voice/IVR, Web, and SMS. It combines AI agricultural advisory (powered by a tiered Claude model router) with financial services — loan eligibility, crop insurance, input financing, and market linkage — all grounded by RAG knowledge retrieval, a modular prompt architecture, and rule-based intent classification.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | FastAPI (async) |
| LLM | Claude Haiku / Sonnet / Opus (tiered model router) |
| Embeddings | Voyage-3 (future RAG) |
| Vector DB | Weaviate (stub for MVP) |
| Cache | Redis (response caching with graceful degradation) |
| Database | PostgreSQL via SQLAlchemy async + asyncpg |
| Migrations | Alembic |

## Prompt Architecture

The system prompt is assembled from 6 modular segments at runtime:

1. **Identity** — who Limi is, capabilities, limitations
2. **Safety Rules** — 8 non-negotiable guardrails (always injected), including FINANCIAL_DISCLOSURE (NCA compliance, APR disclosure, cooling-off period)
3. **Knowledge Context** — RAG-retrieved chunks from DARD/ARC/SAFEX + 6 financial knowledge chunks (NCA, insurance, input financing, market linkage, SARS, stokvels)
4. **Farmer Profile** — personalisation by location, crops, language
5. **Channel Constraints** — formatting per channel (USSD/WhatsApp/IVR/Web/SMS)
6. **Intent Instructions** — behavior per intent category, including 4 financial intent instruction prompts

Assembly order matters: safety rules always before knowledge context for attention priority.

## Request Flow

```
Farmer Message → Channel Router → Intent Classifier → Knowledge Retrieval
    → Prompt Assembly → Model Router → Claude API → Confidence Scoring
    → Response Cache → Token Cost Tracking → DB Persistence → Response
```

## Tiered Model Router

The model router selects a Claude model based on query complexity and stakes:

| Tier | Model | When Used |
|------|-------|-----------|
| Light | Haiku | Simple USSD/SMS queries |
| Standard | Sonnet | Complex agricultural advisory |
| High-Stakes | Opus | Financial intents, high-risk decisions |

## Database Schema

### Core Models
- **FarmerDB** — farmer profiles (location, crops, language, channel preferences)
- **QueryLogDB** — every advisory query with token usage tracking
- **ConversationDB** — conversation session history

### Financial Models
- **FinancialProductDB** — loan, insurance, and savings products
- **FarmerRiskScoreDB** — composite risk scores per farmer
- **TransactionDB** — financial transaction records
- **InputFinancingDB** — input financing applications and status
- **CropInsuranceDB** — crop insurance policies
- **MarketLinkageDB** — buyer/market connections

### Enums
- **FinancialProductType** — loan, insurance, savings, input financing
- **TransactionStatus** — pending, approved, disbursed, repaid, defaulted

The database layer uses graceful degradation: if PostgreSQL is unavailable, the system falls back to seed data and continues operating.

## Farmer Risk Scoring Engine

Composite risk score (0--100) computed from 5 weighted components:

| Component | Weight | Source |
|-----------|--------|--------|
| Farm Profile | 25% | Crop diversity, farm size, irrigation |
| Query Engagement | 25% | Advisory usage frequency and breadth |
| Advisory Compliance | 20% | Follow-through on recommendations |
| Regional Risk | 15% | Province-level agricultural risk index |
| Financial History | 15% | Repayment track record |

The score drives product eligibility matching against 5 seed financial products.

## Response Caching (Redis)

| Intent | TTL |
|--------|-----|
| market_price | 1 hour |
| weather | 1 hour |
| planting_calendar | 24 hours |
| general | 4 hours |
| livestock, disease, financial | Never cached |

Redis is optional; the system degrades gracefully without it.

## Intent Classification

16 intents total — 12 original agricultural intents plus 4 financial intents:

- **LOAN_INQUIRY** — loan eligibility, terms, NCA-compliant disclosure
- **INSURANCE_INQUIRY** — crop insurance products, premiums, coverage
- **SAVINGS_INQUIRY** — savings products, stokvels, interest rates
- **MARKET_LINKAGE** — connecting farmers to buyers and markets

## API Endpoints

### Advisory
- `POST /api/query` — main advisory query endpoint
- `POST /webhooks/whatsapp` — WhatsApp webhook
- `GET /health` — health check

### Financial Services
- `GET /api/financial/products` — all active financial products
- `GET /api/financial/products/{farmer_id}` — eligible products for a farmer
- `GET /api/financial/risk-score/{farmer_id}` — farmer risk score breakdown

### Analytics
- `GET /api/analytics/queries` — query volume over time
- `GET /api/analytics/intents` — intent distribution
- `GET /api/analytics/escalation-rate` — escalation trends
- `GET /api/analytics/unit-economics` — cost per query, cache hit rate
- `GET /api/analytics/funnel` — financial product conversion funnel

## Key Directories

- `app/prompts/` — All 6 prompt segments + assembler
- `app/services/` — Claude orchestration, intent classification, confidence scoring, model routing, risk scoring
- `app/routers/` — FastAPI endpoints (query, WhatsApp webhook, health, financial, analytics)
- `app/models/` — SQLAlchemy DB models (core + financial)
- `knowledge/` — Seed knowledge chunks (JSON) — agricultural + financial
- `tests/` — 108 tests covering assembler, safety, intents, confidence, channels, financial services, analytics, caching, HMAC signature verification, farmer-service helpers (STOP + isiXhosa detection)
- `scripts/` — Operational scripts (e.g., `seed_pilot_farmer.py` for env-driven pilot farmer seeding)

## WhatsApp Inbound Flow (Pilot)

The `/webhook/whatsapp` POST handler is hardened for production with five guarantees:

1. **HMAC signature verification** — every request is verified against `X-Hub-Signature-256` using `WHATSAPP_APP_SECRET` (constant-time compare). Unsigned or tampered requests get 403 in production. In dev (empty `APP_SECRET`), verification is skipped.
2. **5-second SLA via BackgroundTasks** — webhook returns 200 in <50ms; LLM call + send happen asynchronously. Meta retries any webhook taking >5s, which would compound rate-limit and duplicate-message risk.
3. **DB-backed farmer lookup** — `app/services/farmer_service.get_farmer_by_phone()` queries `farmers.external_id` (the WhatsApp E.164 number without `+`). Unregistered numbers receive a "not registered for the pilot" reply without burning Anthropic tokens.
4. **POPIA opt-out** — `STOP` / `cima` / `yima` (exact match after trim+lowercase) deletes the farmer's record and all their `query_logs`, then replies with a deletion confirmation.
5. **isiXhosa code-switching detection** — `farmer_service.detect_isixhosa()` heuristic checks for common Xhosa tokens (greetings, livestock, weather, health) and overrides the farmer's profile-default language for that message. A single Xhosa token in mixed text suffices.

The outbound `whatsapp_sender.send_text` retries 3× on 5xx with exponential backoff, caps body at 4096 chars (WhatsApp's text limit), and logs only a hashed recipient suffix to keep raw phone numbers out of logs.

## Production-mode env validation

`app/main.py:_validate_env()` runs in the FastAPI lifespan startup. When `ENVIRONMENT=production`, missing values for `ANTHROPIC_API_KEY`, `DATABASE_URL`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_APP_SECRET`, or `WHATSAPP_VERIFY_TOKEN` raise `RuntimeError` and prevent the app from starting. Dev mode tolerates blanks for local exploration.

## Deploy target

Pilot deploys to Railway via `railway.toml`:
- Builder: `DOCKERFILE`
- Start command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}` (auto-migrate on every deploy)
- Healthcheck: `/health` (30s timeout)
- Restart: ON_FAILURE up to 3 retries
- Postgres + Redis provisioned as separate Railway services
- Pilot farmer seeded via one-off `python scripts/seed_pilot_farmer.py` from the Railway shell after first deploy
