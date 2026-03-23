import pytest
from app.models.enums import Language, FarmType, SubscriptionTier
from app.models.messages import FarmerProfile, KnowledgeChunk


@pytest.fixture
def kzn_smallholder() -> FarmerProfile:
    return FarmerProfile(
        display_name="Sipho",
        language=Language.ISIZULU,
        province="KwaZulu-Natal",
        district="uMgungundlovu",
        farm_type=FarmType.SMALLHOLDER,
        crops=["maize", "beans", "cabbage"],
        livestock=["cattle", "goats"],
        farm_size_ha=4.5,
        tier=SubscriptionTier.FREE,
        nearest_dard_office="Pietermaritzburg DARD",
        nearest_dard_phone="033 355 9100",
        state_vet_phone="033 845 9801",
    )


@pytest.fixture
def fs_commercial() -> FarmerProfile:
    return FarmerProfile(
        display_name="Johan",
        language=Language.AFRIKAANS,
        province="Free State",
        district="Lejweleputswa",
        farm_type=FarmType.COMMERCIAL,
        crops=["maize", "soybeans", "sunflower", "wheat"],
        livestock=["cattle"],
        farm_size_ha=850,
        tier=SubscriptionTier.PREMIUM,
        nearest_dard_office="Welkom DARD",
        nearest_dard_phone="057 391 7600",
        state_vet_phone="057 391 7700",
    )


@pytest.fixture
def ec_emerging() -> FarmerProfile:
    return FarmerProfile(
        display_name="Nomsa",
        language=Language.ISIXHOSA,
        province="Eastern Cape",
        district="Amathole",
        farm_type=FarmType.EMERGING,
        crops=["maize", "potatoes", "spinach"],
        livestock=["cattle", "sheep", "goats"],
        farm_size_ha=25,
        tier=SubscriptionTier.FREE,
        nearest_dard_office="East London DARD",
        nearest_dard_phone="043 707 5700",
        state_vet_phone="043 707 5800",
    )


@pytest.fixture
def english_farmer() -> FarmerProfile:
    return FarmerProfile(
        display_name="David",
        language=Language.ENGLISH,
        province="Limpopo",
        district="Vhembe",
        farm_type=FarmType.SMALLHOLDER,
        crops=["tomatoes", "maize"],
        livestock=["cattle"],
        farm_size_ha=8,
        tier=SubscriptionTier.FREE,
        nearest_dard_office="Thohoyandou DARD",
        nearest_dard_phone="015 962 1111",
        state_vet_phone="015 962 2222",
    )


@pytest.fixture
def sample_knowledge_chunks() -> list[KnowledgeChunk]:
    return [
        KnowledgeChunk(
            source_title="DARD Maize Production Guidelines",
            source_type="DARD",
            chunk_text="Maize planting in KZN should commence when soil temperature reaches 12°C.",
            relevance_score=0.95,
        ),
        KnowledgeChunk(
            source_title="ARC Northern Corn Leaf Blight Advisory",
            source_type="ARC",
            chunk_text="Northern Corn Leaf Blight is caused by Exserohilum turcicum. Apply triazole fungicide.",
            relevance_score=0.90,
        ),
    ]
