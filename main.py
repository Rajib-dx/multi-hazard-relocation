
import pandas as pd



# Preprocessing
from preprocessing import preprocess_settlements, preprocess_sites

# Settlement engines
from engines.hazard_engine import calculate_hazard_score
from engines.vulnerability_engine import calculate_vulnerability_score
from engines.risk_engine import calculate_risk_score
from engines.relocation_filter import filter_relocation_candidates

# Site engines
from engines.suitability_engine import calculate_site_suitability
from engines.capacity_engine import calculate_carrying_capacity

# Optimization
from optimization.relocation_optimizer import optimize_relocation


# 1. LOAD DATA


settlements = pd.read_csv("data/settlements.csv")
sites = pd.read_csv("data/site.csv")
distances = pd.read_csv("data/distances.csv")



# 2. PREPROCESS DATA


settlements = preprocess_settlements(settlements)
sites = preprocess_sites(sites)

print("\nPREPROCESSED SETTLEMENTS")
print(settlements)

print("\nPREPROCESSED SITES")
print(sites)



# 3. HAZARD ENGINE


settlements = calculate_hazard_score(settlements)

print("\nHAZARD ENGINE OUTPUT")

print(
    settlements[
        [
            "settlement_id",
            "flood_risk_normalized",
            "landslide_risk_normalized",
            "cyclone_risk_normalized",
            "hazard_score"
        ]
    ]
)



# 4. VULNERABILITY ENGINE


settlements = calculate_vulnerability_score(settlements)




print("\nVULNERABILITY ENGINE OUTPUT")





print(
    settlements[
        [
            "settlement_id",
            "population_density_normalized",
            "poverty_normalized",
            "infrastructure_vulnerability",
            "vulnerability_score"
        ]
    ]
)



# 5. MULTI-HAZARD RISK ENGINE


settlements = calculate_risk_score(settlements)

print("\nMULTI-HAZARD RISK ENGINE OUTPUT")

print(
    settlements[
        [
            "settlement_id",
            "hazard_score",
            "vulnerability_score",
            "exposure_score",
            "risk_score",
            "risk_category"
        ]
    ]
)
print(f"imaran: {settlements.columns}")


# 6. RELOCATION FILTER


relocation_candidates = filter_relocation_candidates(settlements)

print("\nSETTLEMENTS REQUIRING RELOCATION")

print(
    relocation_candidates[
        [
            "settlement_id",
            "latitude",
            "longitude",
            "population",
            "risk_score",
            "risk_category"
        ]
    ]
)





# 7. SITE SUITABILITY ENGINE

sites = calculate_site_suitability(sites)

print("\nSAFE SITE SUITABILITY OUTPUT")

print(
    sites[
        [
            "site_id",
            "flood_safety",
            "landslide_safety",
            "slope_suitability",
            "road_access",
            "suitability_score"
        ]
    ]
)


# ==========================================
# 8. CARRYING CAPACITY ENGINE
# ==========================================

sites = calculate_carrying_capacity(sites)

print("\nCARRYING CAPACITY OUTPUT")

print(
    sites[
        [
            "site_id",
            "land_capacity",
            "water_capacity",
            "infrastructure_capacity",
            "carrying_capacity"
        ]
    ]
)



# ==========================================
# 9. RELOCATION OPTIMIZATION
# ==========================================

relocation_plan, updated_sites = optimize_relocation(
    relocation_candidates,
    sites,
    distances
)


# ==========================================
# 10. FINAL OUTPUT
# ==========================================

print("\n================================")
print("FINAL RELOCATION PLAN")
print("================================")

print(relocation_plan)
print(relocation_plan.columns)


print("\n================================")
print("REMAINING SITE CAPACITY")
print("================================")

print(
    updated_sites[
        [
            "site_id",
            "suitability_score",
            "carrying_capacity"
        ]
    ]
)
