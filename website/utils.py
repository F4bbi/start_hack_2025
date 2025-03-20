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

    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        zoom=6.7,
        color="value",
        color_continuous_scale="viridis",
    )
    fig.update_layout(
        height=700,
        xaxis=dict(scaleanchor="y", visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


@st.cache_data
@st.cache_resource
def plot(chart):
    st.plotly_chart(chart, use_container_width=True)
