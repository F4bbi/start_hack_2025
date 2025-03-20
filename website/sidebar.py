import streamlit as st
from utils import SAHEL_LOCATIONS, WEATHER_VARIABLES

def sidebar_controls():
    st.sidebar.title("Settings")

    selected_location = st.sidebar.selectbox(
        "Select location in Sahel region", options=list(SAHEL_LOCATIONS.keys()), index=0
    )

    start_year, end_year = st.sidebar.slider(
        "Select year range", min_value=2020, max_value=2023, value=(2020, 2023)
    )

    selected_temp_var = st.sidebar.selectbox(
        "Select temperature variable",
        options=["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"],
        format_func=lambda x: WEATHER_VARIABLES[x],
        index=2,
    )

    selected_precip_var = st.sidebar.selectbox(
        "Select precipitation variable",
        options=["precipitation_sum", "rain_sum"],
        format_func=lambda x: WEATHER_VARIABLES[x],
        index=0,
    )

    chart_type = st.sidebar.selectbox(
        "Select chart type",
        options=[
            "Temperature & Precipitation",
            "Monthly Comparison",
            "Seasonal Patterns",
            "Annual Cycle",
            "Statistical Distribution",
            "Wind Patterns",
        ],
        index=0,
    )

    return selected_location, start_year, end_year, selected_temp_var, selected_precip_var, chart_type
