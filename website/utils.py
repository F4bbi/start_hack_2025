from pathlib import Path
from enum import Enum
from dataclasses import dataclass

import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.graph_objs import Figure

BASE_DATA_FOLDER = Path("../dataset/csv/")

@dataclass
class DatasetConfig:
    name: str
    column_name: str
    color_scale: str = "viridis"
    color_map: dict | None = None
    value_mapping: dict | None = None

class DatasetType(Enum):
    CLIMATE_PRECIPITATION = DatasetConfig(
        name="🌧️ Precipitation",
        column_name="mm/year"
    )
    GROSS_PRIMARY = DatasetConfig(
        name="⛽️ Gross Primary Production", 
        column_name="kg_C/m²/year"
    )
    LAND_COVER = DatasetConfig(
        name="🌿 Land Cover",
        column_name="Land Type",
        color_scale="discrete",
        value_mapping={
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
        },
        color_map={
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
    )
    POPULATION_DENSITY = DatasetConfig(
        name="🧍🏻 Population Density",
        column_name="people/km²"
    )

DATA_LIST = {
    "climate_precipitation": {"name": DatasetType.CLIMATE_PRECIPITATION.value.name},
    "gross_primary": {"name": DatasetType.GROSS_PRIMARY.value.name},
    "land_cover": {"name": DatasetType.LAND_COVER.value.name},
    "population_density": {"name": DatasetType.POPULATION_DENSITY.value.name},
}

DATASET_MAPPING = {
    "climate_precipitation": DatasetType.CLIMATE_PRECIPITATION,
    "gross_primary": DatasetType.GROSS_PRIMARY,
    "land_cover": DatasetType.LAND_COVER,
    "population_density": DatasetType.POPULATION_DENSITY,
}


@st.cache_data
@st.cache_resource
def create_chart(file: Path) -> Figure:
    df = pd.read_csv(file)
    
    # Get dataset configuration
    dataset_type = DATASET_MAPPING.get(file.parent.name)
    config = dataset_type.value
    
    # Apply value mapping if it exists (for land cover)
    if config.value_mapping:
        df["value"] = df["value"].map(config.value_mapping)
    
    # Rename the column
    df = df.rename(columns={"value": config.column_name})
    color_column = config.column_name
    
    # Set color configuration
    if config.color_scale == "discrete":
        color_scale = None
        color_map = config.color_map
    else:
        color_scale = config.color_scale
        color_map = None

    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        zoom=6.7,
        color=color_column,
        color_continuous_scale=color_scale,
        color_discrete_map=color_map,
        map_style="carto-darkmatter",
        height=700,
    )

    fig.update_traces(marker=dict(size=max(3, 9000 / len(df))))

    return fig


@st.cache_data
@st.cache_resource
def plot(chart: Figure, key: str = ""):
    st.plotly_chart(chart, use_container_width=True, key=key)
