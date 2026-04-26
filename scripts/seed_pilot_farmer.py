"""Seed the pilot farmer into the database.

Reads farmer details from environment variables to keep PII out of source control.
Idempotent — re-running updates the existing record.

Run once after `alembic upgrade head` on each deploy:
    python scripts/seed_pilot_farmer.py

Required env vars:
    PILOT_FARMER_NUMBER     E.164 without '+', e.g. '27782390945'
    PILOT_FARMER_NAME       e.g. 'Khanyiso'

Optional env vars (sensible defaults provided):
    PILOT_FARMER_LANGUAGE   default 'xh'
    PILOT_FARMER_PROVINCE   default 'Eastern Cape'
    PILOT_FARMER_DISTRICT   default 'OR Tambo (Libode/Mthatha)'
    PILOT_FARMER_FARM_TYPE  default 'smallholder'
    PILOT_FARMER_CROPS      comma-separated, default 'cabbage'
    PILOT_FARMER_LIVESTOCK  comma-separated, default 'pigs'
    PILOT_FARMER_SIZE_HA    default '1.5'
"""
import asyncio
import os
import sys

from sqlalchemy import text

from app.db.engine import async_session_factory


async def seed() -> int:
    number = os.environ.get("PILOT_FARMER_NUMBER", "").strip()
    name = os.environ.get("PILOT_FARMER_NAME", "").strip()
    if not number or not name:
        print(
            "ERROR: PILOT_FARMER_NUMBER and PILOT_FARMER_NAME must be set",
            file=sys.stderr,
        )
        return 1
    if async_session_factory is None:
        print("ERROR: DATABASE_URL not configured", file=sys.stderr)
        return 1

    language = os.environ.get("PILOT_FARMER_LANGUAGE", "xh")
    province = os.environ.get("PILOT_FARMER_PROVINCE", "Eastern Cape")
    district = os.environ.get("PILOT_FARMER_DISTRICT", "OR Tambo (Libode/Mthatha)")
    farm_type = os.environ.get("PILOT_FARMER_FARM_TYPE", "smallholder")
    crops = [c.strip() for c in os.environ.get("PILOT_FARMER_CROPS", "cabbage").split(",") if c.strip()]
    livestock = [l.strip() for l in os.environ.get("PILOT_FARMER_LIVESTOCK", "pigs").split(",") if l.strip()]
    size_ha = float(os.environ.get("PILOT_FARMER_SIZE_HA", "1.5"))

    sql = text("""
        INSERT INTO farmers (
            external_id, display_name, language, province, district,
            farm_type, crops, livestock, farm_size_ha, tier
        )
        VALUES (
            :external_id, :display_name, :language, :province, :district,
            :farm_type, :crops, :livestock, :farm_size_ha, 'free'
        )
        ON CONFLICT (external_id) DO UPDATE SET
            display_name = EXCLUDED.display_name,
            language = EXCLUDED.language,
            province = EXCLUDED.province,
            district = EXCLUDED.district,
            farm_type = EXCLUDED.farm_type,
            crops = EXCLUDED.crops,
            livestock = EXCLUDED.livestock,
            farm_size_ha = EXCLUDED.farm_size_ha,
            updated_at = NOW();
    """)

    async with async_session_factory() as session:
        await session.execute(sql, {
            "external_id": number,
            "display_name": name,
            "language": language,
            "province": province,
            "district": district,
            "farm_type": farm_type,
            "crops": crops,
            "livestock": livestock,
            "farm_size_ha": size_ha,
        })
        await session.commit()

    print(f"Seeded pilot farmer: {name} (external_id={number}) — {province}/{district}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(seed()))
