# InDaba — Setup Guide

## Prerequisites

- Python 3.12+
- An Anthropic API key

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

## Running

```bash
uvicorn app.main:app --reload --port 8000
```

## Testing

```bash
pytest tests/ -v
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

### Seed Farmers

- `farmer-001` — Sipho (KZN, isiZulu, smallholder, maize/beans/cabbage)
- `farmer-002` — Johan (Free State, Afrikaans, commercial, maize/soya/wheat)
- `farmer-003` — Nomsa (Eastern Cape, isiXhosa, emerging, maize/potatoes)
