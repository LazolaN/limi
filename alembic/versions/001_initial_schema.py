"""Initial schema — farmers, query_logs, conversations

Revision ID: 001
Revises:
Create Date: 2026-04-03
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Farmers table
    op.create_table(
        "farmers",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("external_id", sa.String(64), unique=True, nullable=False),
        sa.Column("display_name", sa.String(128), nullable=False),
        sa.Column("language", sa.String(4), nullable=False),
        sa.Column("province", sa.String(64), nullable=False),
        sa.Column("district", sa.String(128), nullable=False),
        sa.Column("farm_type", sa.String(20), nullable=False),
        sa.Column("crops", ARRAY(sa.String), nullable=True),
        sa.Column("livestock", ARRAY(sa.String), nullable=True),
        sa.Column("farm_size_ha", sa.Float, nullable=False),
        sa.Column("tier", sa.String(20), server_default="free"),
        sa.Column("nearest_dard_office", sa.String(128), server_default=""),
        sa.Column("nearest_dard_phone", sa.String(20), server_default=""),
        sa.Column("state_vet_phone", sa.String(20), server_default=""),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_farmers_external_id", "farmers", ["external_id"])
    op.create_index("ix_farmers_province", "farmers", ["province"])
    op.create_index("ix_farmers_province_district", "farmers", ["province", "district"])

    # Seed farmers
    op.execute("""
        INSERT INTO farmers (external_id, display_name, language, province, district, farm_type, crops, livestock, farm_size_ha, tier, nearest_dard_office, nearest_dard_phone, state_vet_phone)
        VALUES
        ('farmer-001', 'Sipho', 'zu', 'KwaZulu-Natal', 'uMgungundlovu', 'smallholder', ARRAY['maize','beans','cabbage'], ARRAY['cattle','goats'], 4.5, 'free', 'DARD Pietermaritzburg', '033 355 9100', '033 845 9801'),
        ('farmer-002', 'Johan', 'af', 'Free State', 'Lejweleputswa', 'commercial', ARRAY['maize','soybeans','sunflower','wheat'], ARRAY['cattle'], 850.0, 'premium', 'DARD Welkom', '057 391 7600', '057 391 7700'),
        ('farmer-003', 'Nomsa', 'xh', 'Eastern Cape', 'Buffalo City', 'emerging', ARRAY['maize','potatoes','spinach'], ARRAY['cattle','sheep','goats'], 25.0, 'free', 'DARD East London', '043 707 5700', '043 707 5800')
    """)

    # Query logs table
    op.create_table(
        "query_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("farmer_id", sa.String(64), nullable=False),
        sa.Column("message_id", sa.String(128), nullable=False),
        sa.Column("session_id", sa.String(128), nullable=False),
        sa.Column("intent", sa.String(32), nullable=False),
        sa.Column("confidence", sa.String(8), nullable=False),
        sa.Column("risk_level", sa.String(8), nullable=False),
        sa.Column("channel", sa.String(16), nullable=False),
        sa.Column("language", sa.String(4), nullable=False),
        sa.Column("escalated", sa.Boolean, server_default="false"),
        sa.Column("sources_count", sa.Integer, server_default="0"),
        sa.Column("pipeline_duration_ms", sa.Float, server_default="0"),
        sa.Column("llm_model_used", sa.String(64), server_default=""),
        sa.Column("input_tokens", sa.Integer, server_default="0"),
        sa.Column("output_tokens", sa.Integer, server_default="0"),
        sa.Column("cost_usd_cents", sa.Float, server_default="0"),
        sa.Column("cache_hit", sa.Boolean, server_default="false"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_query_logs_farmer_id", "query_logs", ["farmer_id"])
    op.create_index("ix_query_logs_intent", "query_logs", ["intent"])
    op.create_index("ix_query_logs_farmer_created", "query_logs", ["farmer_id", "created_at"])
    op.create_index("ix_query_logs_intent_created", "query_logs", ["intent", "created_at"])
    op.create_index("ix_query_logs_channel_created", "query_logs", ["channel", "created_at"])

    # Conversations table
    op.create_table(
        "conversations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("farmer_id", sa.String(64), nullable=False),
        sa.Column("session_id", sa.String(128), unique=True, nullable=False),
        sa.Column("channel", sa.String(16), nullable=False),
        sa.Column("started_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("last_message_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("message_count", sa.Integer, server_default="0"),
    )
    op.create_index("ix_conversations_farmer_id", "conversations", ["farmer_id"])
    op.create_index("ix_conversations_session_id", "conversations", ["session_id"])


def downgrade() -> None:
    op.drop_table("conversations")
    op.drop_table("query_logs")
    op.drop_table("farmers")
