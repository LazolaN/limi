# Pilot Deployment — Limi for Lazola's Brother (Mthatha, Libode)

**Pilot scope:** 1 farmer · WhatsApp only · advisory-only (no fintech, no USSD, no vision yet)
**Location:** Mthatha / Libode, OR Tambo District, Eastern Cape
**Operation:** Pig farming + cabbage on ~1ha
**Language:** isiXhosa + English code-switching
**Hosting:** Railway (web + Postgres + Redis)
**LLM:** Anthropic Claude — Sonnet 4.6 default, Haiku 4.5 simple, Opus 4.7 high-stakes

---

## Pre-flight clarifications (Lazola) — done 2026-04-26
- [x] Brother's WhatsApp phone number — captured (kept out of git; lives in Railway env vars only)
- [x] Brother's first name — Khanyiso
- [x] Pig herd size — 2 boars + 5 sows (smallholder breeding herd)
- [x] Farm size — ~1.5ha total (cabbage + pig run combined)

---

## Phase 0 — External setup (Lazola, in parallel with Phase 1)
- [ ] 0.1 Meta Developer account + WhatsApp Cloud API test app — see `docs/meta-whatsapp-setup.md`
- [ ] 0.2 Anthropic API key with monthly spend cap configured in console (suggest US$30/month for pilot)
- [ ] 0.3 Railway account, GitHub connection (free tier OK)

## Phase 1 — Knowledge & code (Claude) — done 2026-04-26
- [x] 1.1 EC pig + cabbage knowledge chunks → `knowledge/seed_chunks.json` (11 new, 22 total)
- [x] 1.2 Meta WhatsApp settings + Anthropic budget cap → `app/config.py`, `.env.example`
- [x] 1.3 `app/services/whatsapp_sender.py` — async Cloud API send + 3-retry exponential backoff + hashed-recipient logs + 4096-char cap
- [x] 1.4 Wire send + HMAC signature verify into `app/routers/whatsapp.py` (BackgroundTasks; webhook returns 200 in <50ms)
- [x] 1.5 DB-backed farmer lookup in `app/services/farmer_service.py` (rejects unknown numbers without burning Anthropic tokens)
- [x] 1.6 isiXhosa code-switching detection (regex-tokenised; matches single Xhosa word in mixed text)
- [x] 1.7 POPIA STOP handler (`STOP` / `cima` / `yima`) — deletes farmer + their query_logs. Auto-consent flow deferred (Khanyiso's consent OOB at registration)
- [x] 1.8 Claude model IDs → Sonnet 4.6 / Opus 4.7 / Haiku 4.5 (kept Haiku at `claude-haiku-4-5-20251001`)
- [x] 1.9 Production-mode env validation in `app/main.py` lifespan (fails fast on missing Meta secrets / Anthropic key / DB URL)
- [x] 1.10 Pilot farmer seeding via `scripts/seed_pilot_farmer.py` — env-driven (no PII in git), idempotent ON CONFLICT (chose this over alembic migration)
- [x] 1.11 Tests: 23 new (7 HMAC signature, 16 farmer-service); 108/108 passing (was 85/85)

## Phase 2 — Deploy
- [ ] 2.1 `railway.toml` + verify Dockerfile is deploy-ready
- [ ] 2.2 Push to GitHub
- [ ] 2.3 Railway: web + managed Postgres + managed Redis + env vars
- [ ] 2.4 First deploy → run `alembic upgrade head`
- [ ] 2.5 `/health` returns 200 with DB + Redis green
- [ ] 2.6 Meta webhook → Railway URL, verify handshake, subscribe to `messages`

## Phase 3 — Smoke test + handoff
- [ ] 3.1 Lazola sends test message → reply received
- [ ] 3.2 Allowlist brother's number on Meta test cohort
- [ ] 3.3 Brother sends `molo` → consent + welcome reply
- [ ] 3.4 Brother sends pig question (e.g., ASF symptom) → ASF chunk surfaces, escalation triggers
- [ ] 3.5 Brother sends cabbage question (e.g., DBM, soil pH) → EC-specific reply
- [ ] 3.6 Send `STOP` → confirmation reply, DB rows deleted
- [ ] 3.7 Inspect `query_logs`: latency, cost per query, no 5xx in Railway logs

## Phase 4 — Iterate (week 1, daily)
- [ ] 4.1 Daily review of `query_logs` for first 7 days
- [ ] 4.2 Add knowledge chunks for any topic that surfaces poorly
- [ ] 4.3 Tune intent classifier if Xhosa code-switching trips it
- [ ] 4.4 Track per-day token spend vs budget cap

## Mandatory doc updates (per global CLAUDE.md, after each phase)
- [ ] D.1 `docs/build-progress.md` — log WhatsApp send, signature verify, Railway deploy as done
- [ ] D.2 `docs/architecture.md` — sender service, signature flow, DB-backed farmer lookup, STOP/POPIA flow
- [ ] D.3 `docs/setup-guide.md` — Railway deploy steps, Meta webhook configuration

---

## Decisions log
- **2026-04-26**: Pilot scoped to advisory only (fintech leg deferred 6–9 months pending NCA/FSCA partnerships)
- **2026-04-26**: Hosting = Railway (chosen over Fly.io for lower-friction managed services at this scale; revisit at 50+ users)
- **2026-04-26**: Fail-fast env validation only when `ENVIRONMENT=production`; dev tolerates blanks
- **2026-04-26**: WhatsApp send via BackgroundTasks (not async sender thread) to keep webhook handler ≤200 LOC and meet Meta's 5s response SLA

## Out of scope for this pilot (explicit)
- USSD, voice/IVR, vision (crop disease photo) — defer until ≥50 farmers
- Vector RAG (Weaviate + Voyage-3) — keyword retrieval acceptable for one user with curated chunks
- Real SAFEX feed — hardcoded prices acceptable; flag honestly in responses
- Financial product origination — eligibility display only, no application workflow
- Sentry/APM — Railway logs + manual review for the first month
