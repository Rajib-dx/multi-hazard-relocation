import pandas as pd


def optimize_relocation(
    relocation_candidates,
    sites,
    distances
):

    assignments = []

    # Prefer road distance, which is supplied by the current dataset and is
    # more meaningful for relocation planning. Retain ``distance_km`` support
    # for older datasets.
    distance_column = next(
        (
            column
            for column in ("road_distance_km", "distance_km", "straight_line_distance_km")
            if column in distances.columns
        ),
        None,
    )
    if distance_column is None:
        raise ValueError(
            "Distance data must include road_distance_km, distance_km, "
            "or straight_line_distance_km."
        )

    # Sort settlements by risk:
    # CRITICAL / highest risk settlements get priority
    candidates = relocation_candidates.sort_values(
        by="risk_score",
        ascending=False
    )

    # Work with remaining site capacities
    sites = sites.copy()

    for _, settlement in candidates.iterrows():

        settlement_id = settlement["settlement_id"]
        population = settlement["population"]

        # Get distances for this settlement
        settlement_distances = distances[
            distances["settlement_id"] == settlement_id
        ]

        possible_sites = []

        for _, site in sites.iterrows():

            site_id = site["site_id"]

            # Find distance between settlement and site
            distance_row = settlement_distances[
                settlement_distances["site_id"] == site_id
            ]

            # Skip if no distance data exists
            if distance_row.empty:
                continue

            distance_km = distance_row.iloc[0][distance_column]

            # Constraint 1:
            # Site must have enough remaining capacity
            if site["carrying_capacity"] < population:
                continue

            # Constraint 2:
            # Site must meet minimum suitability
            if site["suitability_score"] < 50:
                continue

            possible_sites.append({
                "site_id": site_id,
                "site_latitude": site["latitude"],
                "site_longitude": site["longitude"],
                "distance_km": distance_km,
                "suitability_score": site["suitability_score"],
                "carrying_capacity": site["carrying_capacity"]
            })

        # If no suitable site exists
        if not possible_sites:

            assignments.append({
                "settlement_id": settlement_id,
                "settlement_latitude": settlement["latitude"],
                "settlement_longitude": settlement["longitude"],
                "population": population,
                "assigned_site": None,
                "site_latitude": None,
                "site_longitude": None,
                "distance_km": None,
                "status": "NO SUITABLE SITE"
            })

            continue

        # Choose best site.
        # Prototype priority:
        # 1. Higher suitability
        # 2. Shorter distance
        possible_sites = sorted(
            possible_sites,
            key=lambda x: (
                -x["suitability_score"],
                x["distance_km"]
            )
        )

        selected_site = possible_sites[0]

        # Deduct population from site's remaining capacity
        sites.loc[
            sites["site_id"] == selected_site["site_id"],
            "carrying_capacity"
        ] -= population

        assignments.append({
            "settlement_id": settlement_id,
            "settlement_latitude": settlement["latitude"],
            "settlement_longitude": settlement["longitude"],
            "population": population,
            "assigned_site": selected_site["site_id"],
            "site_latitude": selected_site["site_latitude"],
            "site_longitude": selected_site["site_longitude"],
            "distance_km": selected_site["distance_km"],
            "site_suitability": selected_site["suitability_score"],
            "status": "ASSIGNED"
        })

    return pd.DataFrame(assignments), sites
