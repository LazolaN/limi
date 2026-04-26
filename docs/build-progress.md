# Limi — Build Progress

## MVP Sprint ✅

**Status**: Complete — 37 tests passing, server runs, all endpoints functional

### What was built
- **Modular prompt architecture** — 6 segments (identity, safety, knowledge, farmer profile, channel, intent) assembled at runtime
- **7 safety rules** — chemical safety, veterinary boundaries, confidence disclosure, no financial guarantees, poison prevention, cultural sensitivity, data boundaries
- **5 channel formatters** — USSD (160 chars), WhatsApp (4096 chars), Voice/IVR (spoken language), Web (markdown), SMS (alerts)
- **12 intent classifiers** — rule-based keyword matching in English, isiZulu, isiXhosa
- **Confidence scoring** — extracts self-reported labels, overrides based on knowledge availability and hedging language
- **Escalation logic** — automatic escalation for LOW confidence or MEDIUM + HIGH risk
- **18-term agricultural terminology** — verified isiZulu and isiXhosa terms injected for those languages
- **4 few-shot examples** — disease ID (isiZulu/WhatsApp), livestock emergency (English/USSD), market price, low confidence
- **11 seed knowledge chunks** — real SA agricultural content from DARD, ARC, SAFEX
- **3 seed farmer profiles** — Sipho (KZN), Johan (Free State), Nomsa (Eastern Cape)
- **Claude service** — full orchestration pipeline with error handling and structured logging
- **WhatsApp webhook** — verification + message parsing (MVP stub for sending)
- **37 tests** — assembler validation, safety rule regression, intent classification, confidence scoring, channel formatting

## Competitive Landscape Research (April 2026)

**Status**: Complete — documented in `docs/competitive-landscape.md`

### Key findings
- **No direct SA competitor**: No AI-powered conversational agricultural advisory exists for South African emerging farmers in SA languages
- **Two major pan-African threats**: Virtual Agronomist (iSDA, 850K+ users) and Farmer.Chat (Digital Green, 830K+ users) are the largest WhatsApp-based AI advisory platforms in Africa but do not serve SA specifically
- **Funding environment**: African agritech equity funding has declined from $328M (2022) to ~$80M (2025); debt and grants now dominate
- **Strategic priorities**: Telco partnership (Vodacom/MTN), DARD pilot, more SA languages, real-time SAFEX integration, DFI/foundation funding

## Brand Rename: InDaba → Limi (April 2026)

**Status**: Complete — all 37 tests passing after rename

### What changed
- Renamed product from "InDaba" to "Limi" (from "umlimi" — the farmer — in isiZulu)
- Updated all Python models: `InDabaMessage` → `LimiMessage`, `query_indaba` → `query_limi`
- Updated all logger names: `indaba.*` → `limi.*`
- Updated identity prompt with new name and etymology
- Updated all frontend references (sidebar, chat input, placeholders, page title)
- Updated all documentation
- Updated verify token: `indaba-verify-token` → `limi-verify-token`
- Tagline: "Your Farm Advisor"

## Embedded Agri-Fintech Platform (April 2026)

**Status**: Complete — 108/108 tests passing (up from 37), all endpoints functional

Limi evolved from a pure agricultural advisory MVP into an embedded agri-fintech platform across 6 phases.

### Phase 1: Data Persistence Layer
- SQLAlchemy async + asyncpg + Alembic migrations
- DB models: FarmerDB, QueryLogDB, ConversationDB
- Graceful degradation — the app works without a database, falling back to seed data
- Token usage tracking from Anthropic API responses
- Query log persistence on each advisory query

### Phase 2: Financial Domain + New Intents
- 4 new intents: LOAN_INQUIRY, INSURANCE_INQUIRY, SAVINGS_INQUIRY, MARKET_LINKAGE
- Safety Rule 8: FINANCIAL_DISCLOSURE (NCA compliance, APR disclosure, cooling-off period)
- Financial DB models: FinancialProductDB, FarmerRiskScoreDB, TransactionDB, InputFinancingDB, CropInsuranceDB, MarketLinkageDB
- 6 financial knowledge chunks (NCA, insurance, input financing, market linkage, SARS, stokvels)
- 4 financial intent instruction prompts
- Financial few-shot examples (loan isiZulu/WhatsApp, insurance English/Web)
- FinancialProductType and TransactionStatus enums

### Phase 3: Tiered Model Router + Redis Cache
- Model router: Haiku for simple USSD/SMS, Sonnet for complex advisory, Opus for high-stakes financial
- Redis response cache with graceful degradation (works without Redis)
- Cacheable intents: market_price (1h), planting_calendar (24h), weather (1h), general (4h)
- Never cached: livestock, disease, financial intents
- Token cost tracker (per-query cost estimation in USD cents)

### Phase 4: Farmer Risk Scoring Engine
- Composite risk score (0--100) from 5 weighted components
- Farm profile (25%), query engagement (25%), advisory compliance (20%), regional risk (15%), financial history (15%)
- Province-level agricultural risk index
- Product eligibility matcher with 5 seed financial products

### Phase 5: Financial + Analytics API Endpoints
- `GET /api/financial/products` — all active products
- `GET /api/financial/products/{farmer_id}` — eligible products for a farmer
- `GET /api/financial/risk-score/{farmer_id}` — farmer risk score breakdown
- `GET /api/analytics/queries` — query volume over time
- `GET /api/analytics/intents` — intent distribution
- `GET /api/analytics/escalation-rate` — escalation trends
- `GET /api/analytics/unit-economics` — cost per query, cache hit rate
- `GET /api/analytics/funnel` — financial product conversion funnel

### Phase 6: Frontend Updates
- FinancialPanel in sidebar (risk score + eligible products per farmer)
- AnalyticsDashboard tab (KPIs, intent distribution, funnel, unit economics)
- Chat/Analytics tab toggle in header
- Financial quick actions (loan, insurance, buyer)
- "Tiered AI" badge replacing "Claude Sonnet 4"

### What's next
- Weaviate vector search replacing keyword-based knowledge retrieval
- WhatsApp Cloud API integration for sending responses
- Vision model integration for crop disease photos
- Africa's Talking USSD API integration
- Voice/IVR with speech-to-text
- Real SAFEX market price feed integration
- Telco partnership (Vodacom/MTN) for USSD billing
- DARD pilot programme

## Investor Explainer Document (April 2026)

**Status**: Complete — `docs/investor-explainer.md`

Comprehensive product overview covering: feature breakdown (16 intents, 5 channels, 5 languages, 8 safety rules), commercial model (5 financial products with revenue projections), risk scoring engine, unit economics, competitive landscape, go-to-market strategy, regulatory compliance (NCA, FSCA, POPIA), and investment ask (R5-15M seed round).

## Pilot Deployment Hardening (April 2026)

**Status**: In progress — preparing one-farmer pilot in Mthatha / Libode (OR Tambo, Eastern Cape). Pig farming + cabbage on ~1.5ha. Mixed isiXhosa/English code-switching on WhatsApp.

### What was built

**WhatsApp send + security**
- `app/services/whatsapp_sender.py` — async Cloud API send (`graph.facebook.com/v21.0`) with 3-attempt exponential backoff on 5xx, structured logs (recipient hashed for PII safety), 4096-char text limit cap
- HMAC SHA-256 signature verification (`X-Hub-Signature-256`) using `WHATSAPP_APP_SECRET`; constant-time compare; rejects tampered or unsigned requests in production
- Webhook handler refactored to use FastAPI `BackgroundTasks` so POST returns 200 in <50ms (Meta's 5s SLA); LLM call + send happen async

**Pilot user flow**
- DB-backed farmer lookup in `app/services/farmer_service.py` — replaces in-memory `SEED_FARMERS` dict for the WhatsApp path; unregistered numbers are rejected with a "not registered" reply (no Anthropic tokens burned)
- isiXhosa code-switching detection — heuristic on common Xhosa tokens (greetings, livestock, weather, health); a single Xhosa token in mixed text detects as Xhosa
- POPIA opt-out: `STOP` / `cima` / `yima` deletes farmer + all query_logs, replies with confirmation
- Query log persistence wired into the WhatsApp path (matches the `/api/query` web path), with per-message cost tracking via `estimate_cost`

**Knowledge expansion (11 new EC chunks)**
- DALRRD ASF + biosecurity for Eastern Cape (OR Tambo, Alfred Nzo, Joe Gqabi outbreak history)
- DALRRD swill-feeding regulations under Animal Diseases Act 35 of 1984
- ARC pig vaccination schedule (CSF, erysipelas, parvo/lepto) — explicit no-ASF-vaccine warning
- ARC subtropical pig housing + low-cost smallholder rations
- DRDAR EC cabbage variety guide (Glory of Enkhuizen, Drumhead, Conquistador, Hercules) with planting windows for Mthatha
- DRDAR diamondback moth IPM (Bt, Spinosad, Indoxacarb rotation) + black rot + bacterial soft rot
- DRDAR EC acidic-soil liming guide (pH 4.5-5.5 typical for Libode)
- Mthatha NFPM + NSNP + retail market channels for cabbage; live auction + butchery + weaner channels for pigs
- EC State Vet + DALRRD reporting protocol

**Configuration & infrastructure**
- Updated Claude model IDs to current: Sonnet 4.6, Opus 4.7, Haiku 4.5
- Added `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_APP_SECRET`, `WHATSAPP_API_BASE_URL`, `ANTHROPIC_MONTHLY_BUDGET_USD` to `Settings`
- Default `WHATSAPP_VERIFY_TOKEN` reduced from `"limi-verify-token"` to empty string — forces explicit configuration
- Production-mode env validation (`_validate_env` in `app/main.py` lifespan) — fails fast if `ANTHROPIC_API_KEY`, `DATABASE_URL`, or any Meta secret is missing when `ENVIRONMENT=production`
- `scripts/seed_pilot_farmer.py` — env-driven, idempotent INSERT … ON CONFLICT for the pilot farmer record (keeps PII out of git history)
- `railway.toml` — Dockerfile builder, auto-migrate on deploy (`alembic upgrade head &&` in startCommand), `/health` healthcheck, restart on failure
- `docs/meta-whatsapp-setup.md` — 9-step crib sheet for Meta Cloud API test app (no Business Verification needed for ≤5 test recipients)

**Tests added (23 new, 108 total passing)**
- 7 HMAC signature tests (valid, tampered body, wrong secret, missing header, missing secret, wrong algorithm, empty body)
- 16 farmer-service tests (STOP variants in EN + isiXhosa + edge cases; isiXhosa detection on greetings, code-switched text, punctuation, pure English negative)

### Out of scope for this pilot (explicit)
- USSD / Voice / SMS channels — defer until ≥50 farmers
- Vector RAG (Weaviate + Voyage-3) — keyword retrieval acceptable for one curated cohort
- Real SAFEX feed — hardcoded prices acceptable; honest hedging in responses
- Vision (crop disease photo) — defer; pigs and cabbage have well-known visual symptoms but the LLM-only path is fine for one user
- Financial product origination — eligibility display only; partnerships not signed
- Sentry / APM — Railway logs sufficient for first month
- First-message auto-consent flow — Khanyiso's consent is captured out-of-band at registration; the auto-consent code path remains a future improvement for self-onboarding new numbers
