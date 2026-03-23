from app.models.enums import Language, FarmType, SubscriptionTier
from app.models.messages import FarmerProfile

SEED_FARMERS: dict[str, FarmerProfile] = {
    "farmer-001": FarmerProfile(
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
    ),
    "farmer-002": FarmerProfile(
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
    ),
    "farmer-003": FarmerProfile(
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
    ),
}

DEFAULT_FARMER = SEED_FARMERS["farmer-001"]
