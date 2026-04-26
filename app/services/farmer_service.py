"""DB-backed farmer lookup, POPIA opt-out, and isiXhosa language detection."""
import logging
import re
from typing import Optional

from sqlalchemy import text

from app.db.engine import async_session_factory
from app.models.enums import FarmType, Language, SubscriptionTier
from app.models.messages import FarmerProfile

logger = logging.getLogger("limi.farmer")

# Common isiXhosa tokens. Conservative — only triggers on clearly-Xhosa words.
# Mixed code-switching with at least one Xhosa token detects as Xhosa; pure English does not.
_XHOSA_HINTS = {
    # Greetings + politeness
    "molo", "molweni", "enkosi", "ndiyabulela", "kunjani", "unjani",
    "ndicela", "ndifuna", "uxolo", "siyabonga",
    # Question words
    "yintoni", "iphi", "nini", "ngubani", "kanjani", "ngoba",
    # Farm / livestock / crops
    "iinkomo", "ihagu", "iihagu", "ikhabhetshi", "ikhaphetshi",
    "amazimba", "umbona", "izityalo", "isitshalo", "ibhokhwe", "iibhokhwe",
    # Land / weather
    "umhlaba", "umhlabathi", "imvula", "ilanga", "umoya",
    # Common verbs / nouns
    "uthini", "uthe", "uncedo", "wam", "yam", "akho",
    # Health / illness
    "isifo", "ugula", "ufa",
}


def detect_isixhosa(text_in: Optional[str]) -> bool:
    """True if the message contains common isiXhosa tokens.

    Strips punctuation before tokenising so 'Molo!' still matches 'molo'.
    """
    if not text_in:
        return False
    tokens = set(re.findall(r"[a-z]+", text_in.lower()))
    return bool(tokens & _XHOSA_HINTS)


def is_stop_message(body: Optional[str]) -> bool:
    """Recognise POPIA opt-out keywords in English and isiXhosa.

    Exact match only after trim+lowercase — 'stop please help' is NOT an opt-out.
    """
    if not body:
        return False
    return body.strip().lower() in {"stop", "cima", "yima"}


async def get_farmer_by_phone(phone: str) -> Optional[FarmerProfile]:
    """Look up farmer in DB by external_id (phone without leading '+').

    Returns FarmerProfile if found; None if not registered or DB unavailable.
    The router replies with a registration prompt on None — never burns Anthropic
    tokens for unregistered numbers.
    """
    if async_session_factory is None:
        logger.info("farmer_lookup_no_db")
        return None

    sql = text("""
        SELECT display_name, language, province, district, farm_type,
               crops, livestock, farm_size_ha, tier,
               nearest_dard_office, nearest_dard_phone, state_vet_phone
        FROM farmers
        WHERE external_id = :external_id
        LIMIT 1
    """)

    try:
        async with async_session_factory() as session:
            result = await session.execute(sql, {"external_id": phone})
            row = result.first()
    except Exception as exc:
        logger.warning("farmer_lookup_failed error=%s", str(exc))
        return None

    if row is None:
        logger.info("farmer_not_registered phone_suffix=%s", phone[-4:] if len(phone) >= 4 else "")
        return None

    return FarmerProfile(
        display_name=row.display_name,
        language=Language(row.language),
        province=row.province,
        district=row.district,
        farm_type=FarmType(row.farm_type),
        crops=row.crops or [],
        livestock=row.livestock or [],
        farm_size_ha=row.farm_size_ha,
        tier=SubscriptionTier(row.tier or "free"),
        nearest_dard_office=row.nearest_dard_office or "",
        nearest_dard_phone=row.nearest_dard_phone or "",
        state_vet_phone=row.state_vet_phone or "",
    )


async def delete_farmer(phone: str) -> bool:
    """POPIA STOP handler — delete farmer record + their query_logs.

    Returns True if a farmer row was deleted; False if not found or DB unavailable.
    Deletes query_logs first (no FK so order is by convention only).
    """
    if async_session_factory is None:
        return False

    try:
        async with async_session_factory() as session:
            await session.execute(
                text("DELETE FROM query_logs WHERE farmer_id = :phone"),
                {"phone": phone},
            )
            result = await session.execute(
                text("DELETE FROM farmers WHERE external_id = :phone"),
                {"phone": phone},
            )
            await session.commit()
            deleted = (result.rowcount or 0) > 0
            logger.info(
                "farmer_delete deleted=%s phone_suffix=%s",
                deleted,
                phone[-4:] if len(phone) >= 4 else "",
            )
            return deleted
    except Exception as exc:
        logger.warning("farmer_delete_failed error=%s", str(exc))
        return False
