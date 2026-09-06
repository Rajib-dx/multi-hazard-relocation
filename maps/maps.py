from pathlib import Path
import sys
import pandas as pd
import folium

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from main import relocation_candidates


# LOAD DATA


sites = pd.read_csv(
    "data/site.csv"
)

distances = pd.read_csv(
    "data/distances.csv"
)



# CREATE MAP


map_center = [
    relocation_candidates["latitude"].mean(),
   relocation_candidates["longitude"].mean()
]

relocation_map = folium.Map(
    location=map_center,
    zoom_start=10,
    tiles="OpenStreetMap"
)



# SETTLEMENT MARKERS


for _, candidate in relocation_candidates.iterrows():

    popup_text = f"""
    <b>{candidate['settlement_name']}</b><br>

    Population: {candidate['population']}<br>
    Risk score: {candidate['risk_score']:.2f}<br>
    Risk Category: {candidate['risk_category']} <br>
    """

    folium.CircleMarker(
        location=[
            candidate["latitude"],
            candidate["longitude"]
        ],

        radius=20,

        popup=folium.Popup(
            popup_text,
            max_width=300
        ),

        color="red",

        fill=True,

        fill_color="red",

        fill_opacity=0.8

    ).add_to(relocation_map)


# CANDIDATE SITE MARKERS


for _, site in sites.iterrows():

    popup_text = f"""
    <b>{site['site_name']}</b><br>

    Available Land:
    {site['available_land_area']}<br>

    Flood Risk:
    {site['flood_risk']}<br>

    Landslide Risk:
    {site['landslide_risk']}<br>

    Soil Stability:
    {site['soil_stability']}<br>

    Water Availability:
    {site['water_availability']}
    """

    folium.Marker(

        location=[
            site["latitude"],
            site["longitude"]
        ],

        popup=folium.Popup(
            popup_text,
            max_width=300
        ),

        icon=folium.Icon(
            color="green",
            icon="home"
        )

    ).add_to(relocation_map)



# NEAREST SITE FOR EACH SETTLEMENT


for _, candidate in relocation_candidates.iterrows():

    settlement_distances = distances[
        distances["settlement_id"]
        == candidate["settlement_id"]
    ]

    nearest_site_row = (
        settlement_distances
        .sort_values(
            "road_distance_km"
        )
        .iloc[0]
    )

    site_id = nearest_site_row["site_id"]

    site = sites[
        sites["site_id"] == site_id
    ].iloc[0]


    folium.PolyLine(

        locations=[
            [
                candidate["latitude"],
                candidate["longitude"]
            ],

            [
                site["latitude"],
                site["longitude"]
            ]
        ],

        color="blue",

        weight=3,

        opacity=0.7,

        popup=(
            f"{candidate['settlement_name']}"
            f" → "
            f"{site['site_name']}"
            f"<br>"
            f"Estimated Road Distance: "
            f"{nearest_site_row['road_distance_km']} km"
        )

    ).add_to(relocation_map)


# SAVE MAP


relocation_map.save(
    "maps/relocation_map.html"
)

print(
    "Relocation map generated successfully."
)