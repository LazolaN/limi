# InDaba — Architecture

## Overview

InDaba is an AI agricultural advisory agent serving South African farmers via WhatsApp, USSD, Voice/IVR, Web, and SMS. It uses Claude Sonnet 4 with RAG grounding, a modular prompt architecture, and rule-based intent classification.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | FastAPI (async) |
| LLM | Claude Sonnet 4 via Anthropic SDK |
| Embeddings | Voyage-3 (future RAG) |
| Vector DB | Weaviate (stub for MVP) |
| Cache | Redis (stub for MVP) |
| Database | PostgreSQL (stub for MVP) |

## Prompt Architecture

The system prompt is assembled from 6 modular segments at runtime:

1. **Identity** — who InDaba is, capabilities, limitations
2. **Safety Rules** — 7 non-negotiable guardrails (always injected)
3. **Knowledge Context** — RAG-retrieved chunks from DARD/ARC/SAFEX
4. **Farmer Profile** — personalisation by location, crops, language
5. **Channel Constraints** — formatting per channel (USSD/WhatsApp/IVR/Web/SMS)
6. **Intent Instructions** — behavior per intent category

Assembly order matters: safety rules always before knowledge context for attention priority.

## Request Flow

```
Farmer Message → Channel Router → Intent Classifier → Knowledge Retrieval
    → Prompt Assembly → Claude API → Confidence Scoring → Response
```

## Key Directories

- `app/prompts/` — All 6 prompt segments + assembler
- `app/services/` — Claude orchestration, intent classification, confidence scoring
- `app/routers/` — FastAPI endpoints (query, WhatsApp webhook, health)
- `knowledge/` — Seed knowledge chunks (JSON)
- `tests/` — 37 tests covering assembler, safety, intents, confidence, channels
