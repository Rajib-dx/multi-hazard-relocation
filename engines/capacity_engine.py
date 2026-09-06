def calculate_carrying_capacity(df):


    people_per_hectare = 500
    population_at_full_service = 20_000

    # One hectare supports 500 people in this planning model.
    df["land_capacity"] = df["available_land"] * people_per_hectare

    # Water availability score represents a maximum
    # population support level when the score is 1.0.
    df["water_capacity"] = (
        df["water_availability"] * population_at_full_service
    )

    # Infrastructure capacity based on the weakest
    # essential infrastructure component
    df["infrastructure_capacity"] = (
        df[
            [
                "healthcare_access",
                "education_access",
                "electricity_access"
            ]
        ]
        .mean(axis=1)
        * population_at_full_service
    )

    # Final carrying capacity is constrained by
    # the weakest available resource
    df["carrying_capacity"] = df[
        [
            "land_capacity",
            "water_capacity",
            "infrastructure_capacity"
        ]
    ].min(axis=1)

    # Round capacity to whole people
    df["carrying_capacity"] = (
        df["carrying_capacity"]
        .round()
        .astype(int)
    )

    return df
