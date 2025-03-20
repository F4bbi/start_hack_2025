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


@st.cache_data
@st.cache_resource
def create_chart(file: str) -> Figure:
    df = pd.read_csv(file)

    # df["color_label"] = df["value"].astype(str)

    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        zoom=6.7,
        color="value",
        color_continuous_scale="viridis",
        height=700,
        # category_orders={
        #     "color_label": ["gogo7", "gogo10", "gogo12", "gogo13", "gogo16"]
        # },
    )
    return fig


@st.cache_data
@st.cache_resource
def plot(chart):
    st.plotly_chart(chart, use_container_width=True)
