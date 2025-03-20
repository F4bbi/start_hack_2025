from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.graph_objs import Figure

BASE_DATA_FOLDER = Path("../dataset/csv/")

DATA_LIST = {
    "climate_precipitation": {"name": "Precipitation"},
    "gross_primary": {"name": "Gross primary production"},
    "land_cover": {"name": "Land cover"},
    "population_density": {"name": "Population density"},
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
        height=700,
    )
    return fig


# @st.cache_data
# @st.cache_resource
def plot(chart: Figure):
    st.plotly_chart(chart, use_container_width=True)
