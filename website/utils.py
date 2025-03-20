from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.graph_objs import Figure

BASE_DATA_FOLDER = Path("../dataset/csv/")

DATA_LIST = {
    "climate_precipitation": {"name": "🌧️ Precipitation"},
    "gross_primary": {"name": "⛽️ Gross Primary Production"},
    "land_cover": {"name": "🌿 Land Cover"},
    "population_density": {"name": "🧍🏻 Population Density"},
}

LAND_COVER_TYPES = {
    0: "Water Bodies",
    1: "Evergreen Needleleaf Forests",
    2: "Evergreen Broadleaf Forests",
    3: "Deciduous Needleleaf Forests",
    4: "Deciduous Broadleaf Forests",
    5: "Mixed Forests",
    6: "Closed Shrublands",
    7: "Open Shrublands",
    8: "Woody Savannas",
    9: "Savannas",
    10: "Grasslands",
    11: "Permanent Wetlands",
    12: "Croplands",
    13: "Urban and Built-up Lands",
    14: "Cropland/Natural Vegetation Mosaics",
    15: "Permanent Snow and Ice",
    16: "Barren",
    255: "Unclassified",
}

LAND_COVER_COLORS = {
    "Water Bodies": "#1f77b4",
    "Evergreen Needleleaf Forests": "#7f7f7f",
    "Evergreen Broadleaf Forests": "#2ca02c",
    "Deciduous Needleleaf Forests": "#d62728",
    "Deciduous Broadleaf Forests": "#9467bd",
    "Mixed Forests": "#8c564b",
    "Closed Shrublands": "#e377c2",
    "Open Shrublands": "#ff7f0e",
    "Woody Savannas": "#1f77b4",
    "Savannas": "#17becf",
    "Grasslands": "#64700f",
    "Permanent Wetlands": "#ff7f0e",
    "Croplands": "#bcbd22",
    "Urban and Built-up Lands": "#7f7f7f",
    "Cropland/Natural Vegetation Mosaics": "#9467bd",
    "Permanent Snow and Ice": "#e377c2",
    "Barren": "#8c564b",
    "Unclassified": "#d62728",
}


# @st.cache_data
# @st.cache_resource
def create_chart(file: Path) -> Figure:
    df = pd.read_csv(file)

    if file.parent.name == "land_cover":
        df["value"] = df["value"].map(LAND_COVER_TYPES)

    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        zoom=6.7,
        color="value",
        color_continuous_scale="viridis",
        color_discrete_map=LAND_COVER_COLORS,
        map_style="carto-darkmatter",
        height=700,
    )

    fig.update_traces(marker=dict(size=max(3, 9000 / len(df))))

    return fig


# @st.cache_data
# @st.cache_resource
def plot(chart: Figure, key: str = ""):
    st.plotly_chart(chart, use_container_width=True, key=key)
