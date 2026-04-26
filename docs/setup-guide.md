# Limi — Setup Guide

## Prerequisites

- Python 3.12+
- An Anthropic API key
- PostgreSQL 15+ (optional — the app falls back to seed data without it)
- Redis 7+ (optional — the app works without caching)

## Installation

```bash
cd indaba
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env
# Edit .env and set your ANTHROPIC_API_KEY
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes (prod) | Anthropic API key |
| `ANTHROPIC_MONTHLY_BUDGET_USD` | No | Soft monthly cost ceiling for alerting; default `30` |
| `DATABASE_URL` | Yes (prod) | PostgreSQL connection string (e.g. `postgresql+asyncpg://user:pass@localhost:5432/limi`) |
| `REDIS_URL` | No | Redis connection string (e.g. `redis://localhost:6379/0`) |
| `ENVIRONMENT` | No | `development` (default) or `production`; production triggers fail-fast env validation |
| `WHATSAPP_VERIFY_TOKEN` | Yes (prod) | Random string you set; Meta echoes it during webhook handshake |
| `WHATSAPP_ACCESS_TOKEN` | Yes (prod) | Long-lived System User token from Meta Business Settings |
| `WHATSAPP_PHONE_NUMBER_ID` | Yes (prod) | Meta phone number ID from WhatsApp → API Setup |
| `WHATSAPP_APP_SECRET` | Yes (prod) | App Secret from Meta App Settings → Basic; used for HMAC webhook verification |
| `WHATSAPP_API_BASE_URL` | No | Default `https://graph.facebook.com/v21.0` |

See `docs/meta-whatsapp-setup.md` for the Meta Cloud API onboarding crib sheet.

## PostgreSQL Setup

```bash
# Install PostgreSQL (macOS)
brew install postgresql@15
brew services start postgresql@15

# Create database
createdb limi

# Set DATABASE_URL in .env
# DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/limi
```

### Running Migrations

```bash
# Apply all migrations
alembic upgrade head

# Create a new migration after model changes
alembic revision --autogenerate -m "description of change"

# Check current migration status
alembic current

# Rollback one migration
alembic downgrade -1
```

## Redis Setup

```bash
# Install Redis (macOS)
brew install redis
brew services start redis

# Set REDIS_URL in .env
# REDIS_URL=redis://localhost:6379/0
```

Redis is used for response caching. Without it, every query goes directly to the Claude API. The app starts and runs normally either way.

## Running

```bash
uvicorn app.main:app --reload --port 8000
```

## Testing

```bash
pytest tests/ -v
# Expected: 108 tests passing
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Advisory Query
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "test-001",
    "farmer_id": "farmer-001",
    "channel": "whatsapp",
    "language": "zu",
    "content_type": "text",
    "content": {"text": "Kwenzakalani emibileni yami? Amaqabunga anomgca onsundu."},
    "session_id": "session-001"
  }'
```

### Financial Services

```bash
# All active financial products
curl http://localhost:8000/api/financial/products

# Eligible products for a specific farmer
curl http://localhost:8000/api/financial/products/farmer-001

# Farmer risk score
curl http://localhost:8000/api/financial/risk-score/farmer-001
```

### Analytics

```bash
# Query volume over time
curl http://localhost:8000/api/analytics/queries

# Intent distribution
curl http://localhost:8000/api/analytics/intents

# Escalation rate trends
curl http://localhost:8000/api/analytics/escalation-rate

# Unit economics (cost per query, cache hit rate)
curl http://localhost:8000/api/analytics/unit-economics

# Financial product conversion funnel
curl http://localhost:8000/api/analytics/funnel
```

### Seed Farmers

These three demo farmers are inserted by alembic migration 001 and used by the React web UI:

- `farmer-001` — Sipho (KZN, isiZulu, smallholder, maize/beans/cabbage)
- `farmer-002` — Johan (Free State, Afrikaans, commercial, maize/soya/wheat)
- `farmer-003` — Nomsa (Eastern Cape, isiXhosa, emerging, maize/potatoes)

The **WhatsApp pilot path** does not use these — it queries `farmers.external_id` directly against the inbound phone number (E.164 without `+`).

## Production Deployment (Railway)

The repo includes `railway.toml` configured for Dockerfile builds with auto-migrate on deploy.

### One-time setup

1. **Provision services** in your Railway project:
   - Web service (this repo, auto-deploys from GitHub)
   - PostgreSQL (managed)
   - Redis (managed)

2. **Set environment variables** in the Railway dashboard for the web service:
   ```
   ENVIRONMENT=production
   ANTHROPIC_API_KEY=sk-ant-...
   ANTHROPIC_MONTHLY_BUDGET_USD=30
   DATABASE_URL=<copy from Railway Postgres "Connect" tab; replace prefix with postgresql+asyncpg://>
   REDIS_URL=<copy from Railway Redis "Connect" tab>
   REDIS_CACHE_ENABLED=true
   WHATSAPP_VERIFY_TOKEN=<your random string>
   WHATSAPP_ACCESS_TOKEN=<long-lived System User token>
   WHATSAPP_PHONE_NUMBER_ID=<from Meta API Setup>
   WHATSAPP_APP_SECRET=<from Meta App Settings → Basic>
   PILOT_FARMER_NUMBER=<E.164 without + or spaces>
   PILOT_FARMER_NAME=<first name>
   ```

3. **First deploy**:
   - Railway builds the Docker image, applies `alembic upgrade head` automatically, and starts uvicorn.
   - Verify `/health` returns 200 with both DB and Redis green.

4. **Seed the pilot farmer** (one-off):
   ```bash
   railway run python scripts/seed_pilot_farmer.py
   ```
   Re-run any time the pilot farmer's profile changes — the script is idempotent.

5. **Configure Meta webhook**:
   - Callback URL: `https://<your-railway-app>.up.railway.app/webhook/whatsapp`
   - Verify Token: same string as `WHATSAPP_VERIFY_TOKEN`
   - Subscribe to the `messages` field

### Subsequent deploys

Push to the connected GitHub branch — Railway auto-redeploys, runs migrations, and restarts. No manual seeding needed unless the pilot farmer profile changes.

### Logs and observability

```bash
# Tail Railway logs for the web service
railway logs --tail

# Inspect recent query logs from the DB
railway run python -c "
import asyncio
from sqlalchemy import text
from app.db.engine import async_session_factory
async def main():
    async with async_session_factory() as s:
        rows = await s.execute(text('SELECT created_at, intent, confidence, escalated, cost_usd_cents FROM query_logs ORDER BY created_at DESC LIMIT 20'))
        for r in rows: print(r)
asyncio.run(main())
"
```
