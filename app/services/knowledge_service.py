import json
from pathlib import Path

from app.models.enums import Intent
from app.models.messages import KnowledgeChunk

# Load seed chunks once at module import time.
_SEED_CHUNKS_PATH = Path(__file__).parent.parent.parent / "knowledge" / "seed_chunks.json"
_SEED_CHUNKS: list[KnowledgeChunk] = []

if _SEED_CHUNKS_PATH.exists():
    with open(_SEED_CHUNKS_PATH) as f:
        raw_chunks = json.load(f)
        _SEED_CHUNKS = [KnowledgeChunk(**chunk) for chunk in raw_chunks]

# Map intents to keywords for naive relevance filtering in MVP.
_INTENT_KEYWORDS: dict[Intent, list[str]] = {
    Intent.CROP_DISEASE_ID: ["disease", "blight", "fungus", "leaf", "spot", "symptom", "tomato", "maize"],
    Intent.PEST_MANAGEMENT: ["pest", "insect", "worm", "borer", "aphid", "moth", "tick"],
    Intent.LIVESTOCK_HEALTH: ["cattle", "goat", "sheep", "livestock", "vet", "vaccine", "tick", "disease"],
    Intent.PLANTING_CALENDAR: ["planting", "plant", "sow", "season", "cultivar", "spacing", "seed rate"],
    Intent.MARKET_PRICE: ["safex", "price", "commodity", "market", "futures"],
    Intent.SOIL_FERTILITY: ["soil", "pH", "lime", "fertiliser", "manure"],
    Intent.IRRIGATION_ADVICE: ["irrigation", "water", "drip"],
}


async def retrieve_knowledge(query: str, intent: Intent) -> list[KnowledgeChunk]:
    """
    Retrieve relevant knowledge chunks for the given query and intent.

    MVP: Simple keyword filtering on the seed chunks.
    Production: Voyage-3 embeddings → Weaviate vector search.
    """
    intent_keywords = _INTENT_KEYWORDS.get(intent, [])
    query_lower = query.lower()

    scored_chunks: list[tuple[float, KnowledgeChunk]] = []

    for chunk in _SEED_CHUNKS:
        chunk_lower = chunk.chunk_text.lower()
        score = 0.0

        # Boost if intent keywords match the chunk
        for keyword in intent_keywords:
            if keyword in chunk_lower:
                score += 0.3

        # Boost if query words appear in the chunk
        for word in query_lower.split():
            if len(word) > 3 and word in chunk_lower:
                score += 0.1

        # Include the chunk's base relevance score
        score += chunk.relevance_score * 0.2

        if score > 0.2:
            scored_chunks.append((score, chunk))

    # Sort by score descending, take top 5
    scored_chunks.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored_chunks[:5]]
