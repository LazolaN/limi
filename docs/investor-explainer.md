# Limi — Investor Explainer

**Your Farm Advisor. From Seed to Sale.**

*Comprehensive product overview, commercial model, and investment thesis for Ubuntu Data Solutions' embedded agri-fintech platform.*

---

## Table of Contents

1. [What is Limi?](#1-what-is-limi)
2. [The Problem](#2-the-problem)
3. [The Solution](#3-the-solution)
4. [How It Works — Technical Architecture](#4-how-it-works--technical-architecture)
5. [Feature Breakdown](#5-feature-breakdown)
6. [Financial Products & Revenue Model](#6-financial-products--revenue-model)
7. [Farmer Risk Scoring Engine](#7-farmer-risk-scoring-engine)
8. [Unit Economics](#8-unit-economics)
9. [Market Opportunity](#9-market-opportunity)
10. [Competitive Landscape](#10-competitive-landscape)
11. [Go-to-Market Strategy](#11-go-to-market-strategy)
12. [Regulatory & Compliance](#12-regulatory--compliance)
13. [Technology Stack](#13-technology-stack)
14. [Traction & Current State](#14-traction--current-state)
15. [Roadmap](#15-roadmap)
16. [Investment Ask](#16-investment-ask)
17. [Team](#17-team)
18. [Appendices](#18-appendices)

---

## 1. What is Limi?

**Limi** (from *umlimi* — "the farmer" in isiZulu) is an AI-powered agricultural advisory and embedded finance platform built for South African farmers. Created by **Ubuntu Data Solutions**, Limi delivers expert farming advice and financial services through the channels farmers already use — WhatsApp, USSD, voice calls, web, and SMS — in their own languages.

**The core insight:** Free agricultural advisory is the acquisition channel. Embedded financial products (input financing, crop insurance, market linkage, savings) are the revenue engine. Every advisory conversation generates data that improves financial risk scoring, creating a flywheel that competitors cannot replicate without the same farmer relationships.

### One-Line Pitch

> Limi is the DigiFarm of South Africa — an AI farm advisor that builds trust through free agricultural guidance, then monetises through embedded financial products that help farmers grow and sell their crops.

---

## 2. The Problem

### 2.1 The Extension Officer Gap

South Africa has approximately **3,000 agricultural extension officers** serving **2.5 million smallholder and emerging farmers** — a ratio of 1:833. Farmers in rural KwaZulu-Natal, Eastern Cape, and Limpopo wait weeks or months for basic crop advice. By the time help arrives, the blight has spread, the planting window has closed, or the livestock is dead.

### 2.2 The Financial Exclusion Gap

- **87% of smallholder farmers** in South Africa have no access to formal agricultural credit (Land Bank, 2024)
- **92% have no crop insurance** — one drought wipes out an entire season's income
- Farmers sell at **20-40% below SAFEX prices** through informal channels because they lack market access
- The **R50 billion stokvel economy** shows farmers want to save — they just lack formal, accessible products

### 2.3 The Language & Channel Gap

- **60%+ of SA's farming population** speaks isiZulu, isiXhosa, or Sesotho as their first language
- **~40% of rural farmers** use feature phones, not smartphones — WhatsApp-only solutions exclude the most vulnerable
- No AI agricultural advisory platform serves South Africa specifically, in SA languages, with SA-specific agricultural knowledge (DARD, ARC, SAFEX)

### 2.4 What This Means

Every year, millions of South African farmers make critical decisions — what to plant, when to spray, whether to sell, how to finance inputs — without expert advice, without financial products, and without market access. The result is lower yields, higher losses, and persistent poverty in a country that should be feeding the continent.

---

## 3. The Solution

Limi solves all three gaps with a single, integrated platform:

```
┌─────────────────────────────────────────────────────────┐
│                    FARMER (Any Phone)                    │
│     WhatsApp · USSD · Voice · Web · SMS                 │
│     isiZulu · isiXhosa · English · Afrikaans · Sesotho  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              LIMI AI ADVISORY (FREE)                     │
│  Crop disease ID · Pest management · Market prices       │
│  Planting calendars · Livestock health · Soil/Irrigation │
│  → Builds trust · Collects data · Scores risk            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│           LIMI FINANCIAL PRODUCTS (REVENUE)              │
│  Input Financing · Crop Insurance · Market Linkage       │
│  Harvest Savings · (powered by risk scoring)             │
└─────────────────────────────────────────────────────────┘
```

**Key Principle:** The advisory layer is free. The financial layer generates revenue. The data from advisory conversations powers the financial underwriting. This is the same model that made Apollo Agriculture ($50M+ raised), DigiFarm (4M+ farmers), and Pula ($20M Series B) successful — adapted for South Africa.

---

## 4. How It Works — Technical Architecture

### 4.1 Request Flow

When a farmer sends a message (in any language, on any channel), Limi processes it through a 10-step pipeline:

```
1. RECEIVE      → Message arrives via WhatsApp, USSD, Voice, Web, or SMS
2. CLASSIFY     → Intent classifier identifies what the farmer needs (16 intents)
3. CACHE CHECK  → Check Redis for cached response (stable intents: prices, calendars)
4. RETRIEVE     → Pull relevant knowledge chunks from 17-source knowledge base
5. PRICE CHECK  → Fetch SAFEX commodity prices if market-related query
6. ROUTE        → Select optimal AI model (Haiku/Sonnet/Opus) based on risk + complexity
7. ASSEMBLE     → Build modular prompt (identity + 8 safety rules + knowledge + profile + channel + intent)
8. GENERATE     → Claude AI generates personalised, channel-formatted response
9. SCORE        → Confidence scoring + escalation check
10. RESPOND     → Format for channel, cache if eligible, log to database, return to farmer
```

### 4.2 Tiered AI Model Router

Limi doesn't use one AI model for everything. A cost-optimised router selects the right model for each query:

| Tier | Model | When Used | Max Tokens | Cost per Query |
|------|-------|-----------|------------|----------------|
| **Light** | Claude Haiku | Simple queries on USSD/SMS (weather, calendar, general) | 512 | ~R0.09 (~$0.005) |
| **Standard** | Claude Sonnet | Complex advisory + financial intents (disease, pest, loans, insurance) | 1,024 | ~R0.27 (~$0.015) |
| **Critical** | Claude Opus | High-stakes decisions (livestock emergency, low confidence + high risk, human escalation) | 2,048 | ~R1.80 (~$0.10) |

**Projected cost reduction:** 60-70% vs. single-model approaches, achieved through intelligent routing + response caching.

### 4.3 Response Caching

Stable responses are cached in Redis to eliminate redundant AI calls:

| Intent | Cache Duration | Rationale |
|--------|---------------|-----------|
| Market prices | 1 hour | Prices update daily, not per-query |
| Planting calendar | 24 hours | Seasonal advice is stable |
| Weather forecast | 1 hour | Weather changes slowly |
| General agriculture | 4 hours | General advice is stable |
| Livestock health | **Never** | Every animal emergency is unique |
| Crop disease | **Never** | Every disease presentation differs |
| Financial intents | **Never** | Personalised eligibility required |

**Target cache hit rate:** 40-60% of all queries, reducing cost per query by nearly half.

### 4.4 Modular Prompt Architecture

Every response is assembled from 8 modular segments, injected in a strict priority order:

1. **Identity** — Who Limi is, capabilities, honest limitations
2. **Safety Rules** — 8 non-negotiable guardrails (always first, highest attention weight)
3. **Knowledge Context** — Up to 5 relevant chunks from the 17-source knowledge base
4. **Financial Context** — Eligible products for this farmer (financial intents only)
5. **Farmer Profile** — Name, province, crops, livestock, farm size, tier
6. **Terminology** — Verified agricultural terms in isiZulu/isiXhosa (18 terms)
7. **Channel Constraints** — Formatting rules per channel (160 chars for USSD, rich markdown for web)
8. **Intent Instructions** — Specific behavioural rules for the query type

This architecture means Limi can serve a smallholder isiZulu farmer on USSD with a 160-character crop disease response AND a commercial Afrikaans farmer on web with a 2,000-word technical analysis — from the same system.

---

## 5. Feature Breakdown

### 5.1 Agricultural Advisory (12 Intents)

| Feature | What It Does | Risk Level | Example Query |
|---------|-------------|------------|---------------|
| **Crop Disease ID** | Identifies diseases from descriptions or photos, recommends treatment | HIGH | "My tomato leaves have brown spots" |
| **Pest Management** | Pest identification, spray schedules, withholding periods | HIGH | "What should I spray for stalk borer?" |
| **Livestock Health** | Triage (emergency/urgent/routine), notifiable disease check | HIGH | "My cow is shaking and has foam at mouth" |
| **Market Prices** | SAFEX commodity prices with farm-value contextualisation | LOW | "What is the current maize price?" |
| **Planting Calendar** | Province-specific planting windows with weather adjustment | MEDIUM | "When should I plant maize in KZN?" |
| **Weather Forecast** | Weather-adjusted farming advice | LOW | "Will it rain this week?" |
| **Soil Fertility** | pH management, lime application, fertiliser guidance | MEDIUM | "How do I improve my soil pH?" |
| **Irrigation** | Water management, drip vs. sprinkler, scheduling | MEDIUM | "How much water does maize need?" |
| **Input Sourcing** | Where to buy seeds, fertiliser, chemicals | MEDIUM | "Where can I buy maize seed?" |
| **General Agriculture** | Catch-all for farming questions | LOW | "How do I start a vegetable garden?" |
| **Subscription Mgmt** | Account and tier management | LOW | "Upgrade my account" |
| **Human Escalation** | Connect to extension officer (24hr SLA) | LOW | "I need to speak to an expert" |

### 5.2 Financial Services (4 Intents)

| Feature | What It Does | Risk Level | Example Query |
|---------|-------------|------------|---------------|
| **Loan Inquiry** | Input financing eligibility, NCA-compliant disclosure | MEDIUM | "Can I get a loan for maize seeds?" / "Ngifuna imalimboleko" |
| **Insurance Inquiry** | Index-based crop insurance explanation, premium estimates | MEDIUM | "How do I insure my crop?" / "Umshwalense wesivuno" |
| **Savings Inquiry** | Harvest-cycle savings, stokvel formalisation, bank options | LOW | "How can I save money from my harvest?" / "Ukulondoloza" |
| **Market Linkage** | Connect to verified buyers, SAFEX-referenced pricing | LOW | "Find a buyer for my maize" / "Ngifuna umthengi" |

### 5.3 Multi-Channel Delivery

| Channel | Reach | Format | Key Constraints |
|---------|-------|--------|-----------------|
| **WhatsApp** | Smartphone farmers (~60%) | Rich text, *bold*, _italic_, quick-reply buttons | 4,096 char limit |
| **USSD** | Feature phone farmers (~40%) | Plain text, numbered screens, menu navigation | 160 chars per screen |
| **Voice/IVR** | Illiterate or hands-busy farmers | Natural spoken language, spelled-out numbers | 200 words per segment |
| **Web** | Extension officers, commercial farmers | Full markdown, tables, headers, technical detail | 2,000 words max |
| **SMS** | Alert-only (price alerts, weather warnings) | Ultra-brief, alert format | 160 chars total |

### 5.4 Multi-Language Support

| Language | Code | Speakers (SA) | Agricultural Terminology | Coverage |
|----------|------|---------------|------------------------|----------|
| **isiZulu** | zu | 12.4M (24.4%) | 18 verified terms | Full |
| **isiXhosa** | xh | 8.2M (16.0%) | 18 verified terms | Full |
| **English** | en | 4.9M (9.6%) | Native | Full |
| **Afrikaans** | af | 6.9M (13.5%) | Native | Full |
| **Sesotho** | st | 3.9M (7.7%) | Planned | Partial |

**Bilingual intent classification:** Every financial and agricultural keyword set includes English AND indigenous language equivalents (e.g., "loan" + "imalimboleko", "insurance" + "umshwalense", "buyer" + "umthengi").

### 5.5 Safety & Compliance System

Limi enforces **8 non-negotiable safety rules** on every response, regardless of query type:

| Rule | Purpose | Key Requirement |
|------|---------|-----------------|
| **1. Chemical Safety** | Prevent pesticide misuse | Never recommend dosages without knowledge grounding |
| **2. Veterinary Boundaries** | Detect notifiable diseases | Foot-and-mouth, ASF, avian flu, anthrax, rabies → immediate state vet referral |
| **3. Confidence Disclosure** | Transparency on certainty | Every response labelled HIGH (>85%), MEDIUM (60-85%), or LOW (<60%) |
| **4. No Financial Guarantees** | Prevent misleading claims | "May improve" not "will increase yield by X%" |
| **5. Poison Prevention** | Chemical safety net | Withholding periods, PPE, storage, Poison Centre (0861 555 777) |
| **6. Cultural Sensitivity** | Respect tradition | Never dismiss indigenous knowledge; respect ceremonial livestock |
| **7. Data Boundaries** | Protect farmer privacy | No ID numbers, bank details, or exact GPS; district-level only |
| **8. Financial Disclosure** | NCA compliance | APR disclosure, cooling-off period (5 days), no guaranteed returns, FSCA regulation |

**Why this matters to investors:** Agricultural and financial advice carries liability. A farmer who misapplies pesticide or enters an unsuitable loan based on AI advice is a lawsuit and a headline. Limi's safety architecture is designed to prevent this from day one.

### 5.6 Confidence Scoring & Escalation

Every Limi response includes a confidence assessment:

- **HIGH** (>85%): Well-grounded in knowledge base, clear diagnosis/recommendation
- **MEDIUM** (60-85%): Partially grounded, some inference required
- **LOW** (<60%): Limited knowledge match, farmer should verify with extension officer

**Automatic escalation triggers:**
- LOW confidence on ANY query → escalate
- MEDIUM confidence + HIGH risk (livestock, disease, pest) → escalate
- Farmer requests human help → escalate with 24-hour SLA

This positions Limi as a **force multiplier for extension officers**, not a replacement. Extension officers handle escalations; Limi handles the 80% of queries that don't need human expertise.

---

## 6. Financial Products & Revenue Model

### 6.1 The Business Model

```
FREE ADVISORY → DATA COLLECTION → RISK SCORING → FINANCIAL PRODUCTS → REVENUE
```

| Layer | Function | Cost | Revenue |
|-------|----------|------|---------|
| Advisory (free) | Builds trust, collects farming data | ~R0.27/query (LLM cost) | R0 |
| Risk Scoring | Computes creditworthiness from advisory data | Negligible (local compute) | R0 |
| Financial Products | Offers loans, insurance, market linkage, savings | Partner-dependent | Commission/margin |

### 6.2 Financial Product Catalogue

#### Product 1: Limi Seed Finance

| Attribute | Detail |
|-----------|--------|
| **Type** | Input financing (seeds, fertiliser, crop protection) |
| **Provider** | Limi / MAFISA (government programme) |
| **Target** | Smallholder and emerging farmers |
| **Loan Range** | R1,000 — R50,000 |
| **Interest Rate** | From 12.5% p.a. (subject to individual NCA assessment) |
| **Repayment** | Pay after harvest (4-8 months) |
| **Eligibility** | Farm size 0.5-100 ha, risk score ≥ 25 |
| **Limi Revenue** | 5-8% margin on input package value |

#### Product 2: Limi Commercial Input Credit

| Attribute | Detail |
|-----------|--------|
| **Type** | Seasonal input credit facility |
| **Provider** | Limi / ABSA AgriBusiness |
| **Target** | Commercial farmers |
| **Credit Range** | R50,000 — R500,000 |
| **Interest Rate** | From 10.5% p.a. |
| **Eligibility** | Farm size 50+ ha, commercial farm type, risk score ≥ 25 |
| **Limi Revenue** | Origination fee + interest spread |

#### Product 3: Limi Crop Shield — Maize (Index Insurance)

| Attribute | Detail |
|-----------|--------|
| **Type** | Index-based drought insurance |
| **Provider** | Limi / Pula Advisors |
| **Target** | All farm types |
| **Premium Range** | R200 — R5,000 per season |
| **Payout Trigger** | Cumulative rainfall below threshold (e.g., <200mm Oct-Jan in KZN) |
| **Available In** | KwaZulu-Natal, Free State, Mpumalanga, North West |
| **Limi Revenue** | 15% commission on premium |

#### Product 4: Limi Market Connect

| Attribute | Detail |
|-----------|--------|
| **Type** | Buyer-farmer matching at SAFEX-referenced prices |
| **Provider** | Limi (direct) |
| **Target** | All farm types (min 1 ha) |
| **Process** | Farmer lists crop → matched with buyer → negotiate → Limi facilitates |
| **Pricing** | Farm-gate prices typically 10-15% below SAFEX spot |
| **Limi Revenue** | 2.5% commission on successful sales |

#### Product 5: Limi Harvest Saver

| Attribute | Detail |
|-----------|--------|
| **Type** | Seasonal savings account |
| **Provider** | Limi / TymeBank |
| **Target** | Smallholder and emerging farmers |
| **Deposit Range** | R100 — R100,000 |
| **Interest Rate** | 8.5% p.a. |
| **Access** | Deposit after harvest, withdraw before planting |
| **Limi Revenue** | Revenue share on deposits (partner arrangement) |

### 6.3 Revenue Projections (Illustrative)

**Assumptions:** 10,000 active farmers, 30% financial product uptake, per-season figures.

| Product | Uptake | Avg Transaction | Commission | Revenue/Season |
|---------|--------|----------------|------------|----------------|
| Seed Finance | 2,000 farmers | R5,000 package | 6% margin = R300 | **R600,000** |
| Crop Shield | 1,500 farmers | R400 premium | 15% = R60 | **R90,000** |
| Market Connect | 1,000 farmers | R15,000 harvest | 2.5% = R375 | **R375,000** |
| Harvest Saver | 500 farmers | R3,000 deposit | Revenue share ~R50 | **R25,000** |
| **Total** | | | | **R1,090,000/season** |

Two seasons per year → **~R2.2M annual revenue at 10,000 farmers**.

At 100,000 farmers (2% of SA smallholder market): **~R22M annual revenue**.

Compare this to a R50/month subscription that 98% of farmers won't pay: R0.

---

## 7. Farmer Risk Scoring Engine

### 7.1 Why Risk Scoring Matters

Traditional agricultural lending fails because lenders can't assess farmer creditworthiness. There's no credit bureau for smallholders who've never had a bank loan. Limi solves this by generating a **composite risk score from advisory interaction data** — data that only exists because the farmer uses Limi for free agricultural advice.

### 7.2 Score Components

Limi computes a **0-100 risk score** from five weighted components:

| Component | Weight | What It Measures | Data Source |
|-----------|--------|-----------------|-------------|
| **Farm Profile** | 25% | Farm type, size, crop diversity | Farmer registration |
| **Query Engagement** | 25% | How actively the farmer uses advisory | Query logs (90-day window) |
| **Advisory Compliance** | 20% | Quality of interactions (high confidence ratio, low escalation) | Confidence & escalation logs |
| **Regional Risk** | 15% | Province-level agricultural risk (rainfall, infrastructure, market access) | Static provincial index |
| **Financial History** | 15% | Transaction completion rate | Transaction records |

### 7.3 Scoring Detail

**Farm Profile (0-100 points):**
- Commercial farm: 40 base points
- Emerging farm: 30 base points
- Smallholder: 20 base points
- Size bonus: log₂(hectares) × 5 (capped at 30)
- Crop diversity: 10 points per crop (capped at 30)

**Provincial Risk Index:**

| Province | Risk Score | Rationale |
|----------|-----------|-----------|
| Western Cape | 75 | Reliable rainfall, strong infrastructure |
| Free State | 70 | Major grain belt, good market access |
| Mpumalanga | 70 | Diverse agriculture, decent infrastructure |
| North West | 65 | Grain belt but drought-prone |
| KwaZulu-Natal | 65 | Subtropical, good rainfall but infrastructure gaps |
| Gauteng | 60 | Urban-peri, small farms |
| Limpopo | 55 | Water-scarce, infrastructure challenges |
| Eastern Cape | 50 | Former homeland areas, limited infrastructure |
| Northern Cape | 45 | Arid, irrigation-dependent |

### 7.4 How Risk Score Drives Product Eligibility

The product matcher filters all 5 financial products against each farmer's profile:

1. **Risk score threshold** — Minimum 25 to qualify for any product
2. **Farm type matching** — Smallholder products vs. commercial products
3. **Province matching** — Crop Shield only in maize-growing provinces
4. **Farm size matching** — Min/max hectare requirements per product

**Example: Sipho (Smallholder, KZN, 4.5 ha, risk score 52)**

| Product | Eligible | Reason |
|---------|----------|--------|
| Limi Seed Finance | Yes | Smallholder, 4.5 ha within range, score ≥ 25 |
| Commercial Input Credit | No | Farm type is smallholder, not commercial |
| Crop Shield — Maize | Yes | KZN is eligible province, all farm types |
| Market Connect | Yes | 4.5 ha ≥ 1.0 ha minimum |
| Harvest Saver | Yes | Smallholder eligible, no size minimum |

**Example: Johan (Commercial, Free State, 850 ha, risk score 68)**

| Product | Eligible | Reason |
|---------|----------|--------|
| Limi Seed Finance | No | Farm type is commercial |
| Commercial Input Credit | Yes | Commercial, 850 ha within range |
| Crop Shield — Maize | Yes | Free State eligible |
| Market Connect | Yes | All types, 850 ha within range |
| Harvest Saver | No | Commercial not eligible (targets smallholder/emerging) |

---

## 8. Unit Economics

### 8.1 Cost per Query

| Model Tier | Input Tokens | Output Tokens | Cost (USD) | Cost (ZAR) |
|-----------|-------------|--------------|-----------|-----------|
| **Haiku** | ~2,000 | ~300 | $0.0035 | ~R0.06 |
| **Sonnet** | ~3,000 | ~800 | $0.021 | ~R0.38 |
| **Opus** | ~3,000 | ~1,000 | $0.12 | ~R2.16 |
| **Cache hit** | 0 | 0 | $0.00 | R0.00 |

**Blended cost estimate** (assuming 45% cache, 20% Haiku, 30% Sonnet, 5% Opus):

| Component | Proportion | Cost |
|-----------|-----------|------|
| Cache hits | 45% | R0.00 |
| Haiku queries | 20% | R0.06 |
| Sonnet queries | 30% | R0.38 |
| Opus queries | 5% | R2.16 |
| **Weighted average** | | **~R0.23/query** |

### 8.2 Revenue per Farmer (Annual)

| Metric | Conservative | Moderate | Optimistic |
|--------|-------------|----------|-----------|
| Queries per farmer/week | 2 | 3 | 5 |
| Annual query cost | R24 | R36 | R60 |
| Financial product uptake | 20% | 30% | 50% |
| Revenue per converting farmer | R500 | R750 | R1,200 |
| **Blended revenue per farmer** | **R100** | **R225** | **R600** |
| **Gross margin per farmer** | R76 | R189 | R540 |

### 8.3 Path to Profitability

| Scale | Farmers | Annual Cost | Annual Revenue | Gross Margin |
|-------|---------|-------------|---------------|-------------|
| Pilot | 1,000 | R36,000 | R225,000 | R189,000 |
| Growth | 10,000 | R360,000 | R2,250,000 | R1,890,000 |
| Scale | 100,000 | R3,600,000 | R22,500,000 | R18,900,000 |
| Target | 500,000 | R18,000,000 | R112,500,000 | R94,500,000 |

**Break-even:** ~1,600 farmers at moderate assumptions.

---

## 9. Market Opportunity

### 9.1 Total Addressable Market (South Africa)

| Segment | Farmers | Description |
|---------|---------|-------------|
| Smallholder | ~2,500,000 | < 10 ha, subsistence + small surplus |
| Emerging | ~200,000 | 10-100 ha, developing commercial capability |
| Commercial | ~35,000 | 100+ ha, fully commercial operations |
| **Total** | **~2,735,000** | |

### 9.2 Serviceable Addressable Market

| Segment | Farmers | Rationale |
|---------|---------|-----------|
| Mobile-accessible smallholders | ~1,500,000 | ~60% of smallholders have mobile access |
| Emerging farmers (all) | ~200,000 | Higher digital literacy, smartphones |
| Commercial (premium) | ~10,000 | Willing to pay for AI advisory |
| **SAM** | **~1,710,000** | |

### 9.3 Market Size (Revenue Potential)

| Scenario | Farmers Reached | Revenue per Farmer | Annual Revenue |
|----------|----------------|-------------------|----------------|
| Year 1 (pilot) | 5,000 | R150 | R750,000 |
| Year 2 | 50,000 | R200 | R10,000,000 |
| Year 3 | 200,000 | R250 | R50,000,000 |
| Year 5 | 500,000 | R350 | R175,000,000 |

The agricultural fintech market in sub-Saharan Africa is valued at **$1.6 billion in debt and $80M in equity** (2025), with South Africa being the most developed financial market on the continent.

---

## 10. Competitive Landscape

### 10.1 No Direct SA Competitor

No AI-powered conversational agricultural advisory platform currently serves South African farmers in SA languages (isiZulu, isiXhosa), with SA-specific knowledge (DARD, ARC, SAFEX), across both WhatsApp and USSD.

### 10.2 Competitor Map

| Competitor | Users | Channels | SA Languages | Financial Products | Threat |
|-----------|-------|----------|-------------|-------------------|--------|
| Virtual Agronomist (iSDA) | 850K+ | WhatsApp | No | No | HIGH — could localise |
| Farmer.Chat (Digital Green) | 830K+ | WhatsApp | No | No | HIGH — expanding globally |
| DigiFarm (Safaricom) | 4M+ | USSD/App | No (Kenya) | Yes (credit, insurance) | MEDIUM — Kenya only |
| Apollo Agriculture | 300K+ | SMS/App | No (Kenya) | Yes (credit, insurance) | LOW — finance-first |
| Pula Advisors | 12 countries | Partners | No | Insurance only | LOW — potential partner |
| **Limi** | **MVP** | **All 5** | **Yes (5)** | **Yes (5 products)** | — |

### 10.3 Limi's Defensible Advantages

1. **SA-specific knowledge base** — Real DARD guidelines, ARC research, SAFEX pricing. Not generic global advice.
2. **Indigenous language support** — Verified isiZulu and isiXhosa agricultural terminology. LLM translation produces inaccurate agricultural terms.
3. **Multi-channel from day one** — USSD reaches the 40% of farmers with feature phones. Competitors are WhatsApp-only.
4. **Embedded finance** — Advisory + financial products in one platform. Advisory-only competitors can't monetise. Finance-only competitors can't build trust.
5. **Safety-first architecture** — 8 non-negotiable rules including NCA compliance. This is regulatory readiness, not just a feature.
6. **Data flywheel** — Every advisory query improves risk scoring. This compounds over time and is impossible to replicate without the farmer relationships.

---

## 11. Go-to-Market Strategy

### 11.1 Phase 1: Government Pilot (Months 1-6)

- Partner with **KZN DARD** and **Eastern Cape DRDAR** for a 1,000-farmer pilot
- Frame Limi as a **digital extension officer** that multiplies staff reach
- Government provides: farmer access, credibility, outcome data, procurement path
- **Target:** 100 farmers month 1 → 1,000 by month 6
- **Key metric:** Advisory adoption rate, query frequency, confidence scores

### 11.2 Phase 2: Telco Partnership (Months 4-9)

- Secure partnership with **Vodacom** (VodaPay) or **MTN** (MoMo)
- Pitch: "We provide the AI advisory engine. You provide distribution and zero-rated data. Revenue share on financial products."
- Zero-rated data eliminates the connectivity barrier
- **Target:** LOI by month 6, pilot by month 9

### 11.3 Phase 3: Financial Product Launch (Months 7-12)

- Activate Limi Seed Finance (MAFISA partnership) for pilot farmers
- Launch Crop Shield insurance (Pula Advisors partnership) in KZN and Free State
- Enable Market Connect for grain farmers
- **Target:** 30% financial product uptake among pilot farmers

### 11.4 Phase 4: Scale (Year 2+)

- Expand to all 9 provinces
- Add Sesotho and Setswana languages
- Real-time SAFEX pricing integration
- WhatsApp Cloud API for production messaging
- Vision model for crop disease photo analysis
- **Target:** 50,000 farmers by end of Year 2

---

## 12. Regulatory & Compliance

### 12.1 National Credit Act (NCA)

Limi's Safety Rule 8 (Financial Disclosure) ensures NCA compliance on every financial interaction:

- **Affordability assessment** disclosed as requirement before any credit
- **Cooling-off period** (5 business days, Section 121) stated in every loan interaction
- **Total cost of credit** disclosure required before agreement signing
- **Maximum interest rates** — NCA caps referenced in knowledge base
- Language: "Interest rates and terms are subject to credit assessment under the National Credit Act (NCA)"

### 12.2 Financial Sector Conduct Authority (FSCA)

- Savings products regulated under FSCA
- Limi does not provide financial advice — every financial interaction ends with: "This is information only, not financial advice. Consult a registered financial advisor for personalised recommendations."
- Insurance products distributed through licensed intermediaries (Pula, Old Mutual, Santam)

### 12.3 POPIA (Protection of Personal Information Act)

- Safety Rule 7 (Data Boundaries): No ID numbers, bank details, or exact GPS collected
- District-level location only
- No cross-farmer data sharing

### 12.4 Agricultural Chemicals (Act 36 of 1947)

- Safety Rule 1: No dosages without knowledge grounding
- Safety Rule 5: PPE, withholding periods, poison prevention on every chemical recommendation
- Group 1 restricted pesticides always referred to extension officer

---

## 13. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.12 | Backend |
| **Framework** | FastAPI (async) | High-performance API |
| **LLM** | Claude Haiku / Sonnet / Opus | Tiered AI advisory |
| **Database** | PostgreSQL + SQLAlchemy async | Farmer profiles, query logs, financial records |
| **Migrations** | Alembic | Schema versioning |
| **Cache** | Redis | Response caching (graceful degradation) |
| **Frontend** | React 19 + TypeScript + Vite + Tailwind | Web dashboard |
| **Container** | Docker | Deployment |
| **Vector DB** | Weaviate (planned) | Production RAG |
| **Embeddings** | Voyage-3 (planned) | Semantic search |

### 13.1 Architecture Qualities

- **Graceful degradation** — App runs without PostgreSQL (falls back to seed data) and without Redis (no caching). This means the core advisory works immediately, infrastructure is additive.
- **Async-first** — Every I/O operation is async (database, Claude API, Redis). Handles concurrent farmer queries efficiently.
- **Modular prompts** — Adding a new intent, safety rule, or knowledge source doesn't require changing the core pipeline. Plug in and go.
- **85 automated tests** — Covering intent classification, safety rules, model routing, caching, risk scoring, product matching, and prompt assembly.

---

## 14. Traction & Current State

### 14.1 What's Built

| Component | Status | Detail |
|-----------|--------|--------|
| Core advisory pipeline | Complete | 16 intents, 5 channels, 5 languages |
| Safety system | Complete | 8 rules enforced on every response |
| Knowledge base | Complete | 17 chunks (11 agricultural + 6 financial) |
| Financial products | Complete | 5 products defined, eligibility matching |
| Risk scoring engine | Complete | 5-component composite score |
| Tiered model router | Complete | Haiku/Sonnet/Opus routing |
| Response caching | Complete | Redis with graceful degradation |
| Analytics endpoints | Complete | 5 endpoints (volume, intents, escalation, economics, funnel) |
| Database persistence | Complete | Query logs, farmer profiles, financial transactions |
| Web dashboard | Complete | Chat + analytics tab, financial panel |
| WhatsApp webhook | Stub | Receives messages, doesn't send via Cloud API |
| USSD gateway | Planned | Africa's Talking integration |
| Vision model | Planned | Crop disease photo analysis |
| Real-time SAFEX | Planned | JSE data feed integration |

### 14.2 Test Coverage

- **85 automated tests** passing
- Coverage areas: prompt assembly (6), safety rules (3), intent classification (11 + 9 financial), confidence scoring (11), channel formatting (6), model routing (8), caching (8), risk scoring (10), product matching (8), token tracking (5)

---

## 15. Roadmap

### Near-Term (Months 1-3): Production Readiness

| Item | Priority | Effort | Impact |
|------|----------|--------|--------|
| WhatsApp Cloud API (send/receive) | P0 | 2 weeks | Without this, there's no WhatsApp product |
| Real-time SAFEX price feed | P0 | 2 weeks | Core differentiator |
| Africa's Talking USSD gateway | P1 | 2 weeks | Feature phone access |
| Weather API (SA Weather Service) | P1 | 1 week | High-value feature |
| DARD pilot deployment | P0 | Ongoing | First real users |

### Medium-Term (Months 4-9): Scale

| Item | Priority | Effort | Impact |
|------|----------|--------|--------|
| Weaviate vector search (replace keyword matching) | P1 | 2 weeks | Advisory quality improvement |
| Vision model for crop disease photos | P1 | 3 weeks | Table-stakes feature |
| Additional languages (Sesotho, Setswana) | P2 | 2 weeks | Broader SA market |
| Telco partnership (Vodacom/MTN) | P0 | Ongoing | Distribution |
| Financial product partnerships (MAFISA, Pula) | P0 | Ongoing | Revenue activation |

### Long-Term (Months 10-18): Expansion

| Item | Priority | Effort | Impact |
|------|----------|--------|--------|
| Voice/IVR with speech-to-text | P2 | 4 weeks | Illiterate farmer access |
| Admin dashboard for extension officers | P2 | 3 weeks | Government use case |
| Pan-African expansion (Zambia, Malawi, Kenya) | P3 | TBD | Market expansion |
| Satellite-based crop monitoring | P3 | TBD | Risk scoring improvement |

---

## 16. Investment Ask

### 16.1 Round

**Seed Round: R5-15M ($275K-$825K USD)**

### 16.2 Use of Funds

| Category | Allocation | Purpose |
|----------|-----------|---------|
| Engineering | 40% | WhatsApp integration, SAFEX feed, USSD gateway, vision model |
| Pilot Operations | 25% | DARD pilot, farmer onboarding, field agents |
| Partnerships | 15% | Telco (Vodacom/MTN), financial product partners (MAFISA, Pula, TymeBank) |
| Cloud & Infrastructure | 10% | Anthropic API, PostgreSQL, Redis, hosting |
| Legal & Compliance | 10% | NCA compliance audit, FSCA registration, POPIA compliance |

### 16.3 Milestones for Next Round

| Milestone | Target | Timeline |
|-----------|--------|----------|
| Production deployment | WhatsApp + USSD live | Month 3 |
| DARD pilot | 1,000 active farmers | Month 6 |
| Financial product activation | First loan disbursed | Month 8 |
| Unit economics proven | Revenue > cost per farmer | Month 10 |
| Series A readiness | 10,000+ farmers, R2M+ ARR | Month 18 |

### 16.4 Target Investors

| Type | Examples | Fit |
|------|---------|-----|
| **DFIs** | IFC, BII (British International Investment), Swedfund | Food security, smallholder inclusion mandate |
| **Foundations** | Gates Foundation, Mastercard Foundation, Rockefeller | Digital agriculture, African development |
| **Impact VCs** | Knife Capital, 4Di Capital, E4E Africa | SA-focused, tech-for-good mandate |
| **Corporate VC** | Vodacom Ventures, Standard Bank VC | Strategic distribution + financial products |
| **Agri-focused** | AgFunder, Omnivore | Sector specialists |

---

## 17. Team

**Ubuntu Data Solutions** — South African AI company building data-driven solutions for African agriculture.

*(Team details to be added — founder bios, domain expertise, technical backgrounds)*

---

## 18. Appendices

### A. Seed SAFEX Commodity Prices (as at 22 March 2026)

| Commodity | Contract | Price (R/ton) | Daily Change |
|-----------|----------|--------------|-------------|
| White Maize | Jul 2026 | R4,850 | -1.2% |
| Yellow Maize | Jul 2026 | R4,720 | -0.8% |
| Soybeans | May 2026 | R8,920 | +0.5% |
| Wheat | Jul 2026 | R6,350 | -0.3% |
| Sunflower | May 2026 | R7,800 | +1.1% |

Farm-gate prices are typically 10-15% below SAFEX spot, accounting for transport, handling, and quality discounts.

### B. Seed Farmer Profiles

| Farmer | Province | Language | Farm Type | Size | Crops | Tier |
|--------|----------|----------|-----------|------|-------|------|
| Sipho | KwaZulu-Natal | isiZulu | Smallholder | 4.5 ha | Maize, beans, cabbage | FREE |
| Johan | Free State | Afrikaans | Commercial | 850 ha | Maize, soya, sunflower, wheat | PREMIUM |
| Nomsa | Eastern Cape | isiXhosa | Emerging | 25 ha | Maize, potatoes, spinach | FREE |

### C. API Endpoint Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check with DB/Redis status |
| POST | `/api/query` | Main advisory query |
| GET | `/webhook/whatsapp` | WhatsApp verification |
| POST | `/webhook/whatsapp` | WhatsApp message handling |
| GET | `/api/financial/products` | All active financial products |
| GET | `/api/financial/products/{farmer_id}` | Eligible products for farmer |
| GET | `/api/financial/risk-score/{farmer_id}` | Farmer risk score |
| GET | `/api/analytics/queries` | Query volume over time |
| GET | `/api/analytics/intents` | Intent distribution |
| GET | `/api/analytics/escalation-rate` | Escalation trends |
| GET | `/api/analytics/unit-economics` | Cost per query, cache rate |
| GET | `/api/analytics/funnel` | Financial product conversion funnel |

### D. Knowledge Base Sources

| Source | Type | Chunks | Topics |
|--------|------|--------|--------|
| DARD (Dept of Agriculture) | Agricultural | 5 | Maize, tomato, potato, goat, soil |
| ARC (Agricultural Research Council) | Agricultural | 3 | Cattle, tick-borne disease, corn leaf blight |
| SAFEX/JSE | Market | 1 | Commodity pricing and trading |
| Other Agricultural | Agricultural | 2 | General crop and livestock guidance |
| NCA | Financial | 1 | National Credit Act for agricultural lending |
| Insurance | Financial | 1 | Index-based crop insurance in SA |
| Finance | Financial | 2 | Input financing for smallholders, stokvels/savings |
| SAFEX | Financial | 1 | Market linkage and commodity trading |
| SARS | Financial | 1 | Tax implications for farm income |
| **Total** | | **17** | |

---

*This document reflects the Limi platform as built (commit history through April 2026). All features described are implemented in the codebase with 85 passing automated tests. Financial product terms are illustrative and subject to partner agreements.*

*Prepared by Ubuntu Data Solutions. Contact: [to be added]*
