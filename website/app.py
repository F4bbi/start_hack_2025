import pandas as pd
import plotly.express as px
import streamlit as st

from data_processor import (
    create_annual_cycle_chart,
    create_combined_chart,
    create_monthly_comparison_chart,
    create_seasonal_heatmap,
    create_wind_rose_chart,
    create_yearly_comparison_boxplot,
)
from utils import (
    SAHEL_LOCATIONS,
    WEATHER_VARIABLES,
    get_historical_weather_data,
    get_sahel_info,
)

# Configure page
st.set_page_config(
    page_title="Sahel Desert Weather Visualization",
    page_icon="🏜️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("🏜️ Sahel Desert Weather Visualization")
st.markdown("""
    Explore the weather patterns of the Sahel desert region through interactive visualizations.
    This dashboard provides insights into temperature, precipitation, humidity, and wind patterns
    throughout the year across multiple locations in the Sahel.
""")

# Sidebar
st.sidebar.title("Settings")

# Location selection
selected_location = st.sidebar.selectbox(
    "Select location in Sahel region", options=list(SAHEL_LOCATIONS.keys()), index=0
)

# Year range
start_year, end_year = st.sidebar.slider(
    "Select year range", min_value=2020, max_value=2023, value=(2020, 2023)
)

# Variables to display
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

# Chart type selection
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

# Show basic info about the data
st.markdown(f"### Weather data for {selected_location} ({start_year}-{end_year})")

# Display selected chart based on user choice
if chart_type == "Temperature & Precipitation":
    uploaded_file = st.file_uploader("Carica un file CSV", type="csv")

    df = pd.read_csv(uploaded_file)

    # Creare il grafico, senza arrotondare i valori
    fig = px.scatter(
        df,
        x="lon",
        y="lat",
        color="precipitation",
        color_continuous_scale="viridis",
    )

    # Nascondere gli assi e sfondo
    fig.update_layout(
        height=600,
        xaxis=dict(scaleanchor="y", visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Mostrare il grafico
    st.plotly_chart(fig, use_container_width=True)

    # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

    # st.plotly_chart(
    #     create_combined_chart(df, selected_temp_var, selected_precip_var),
    #     use_container_width=True,
    # )

    st.markdown("""
    This chart shows the relationship between temperature and precipitation throughout the year.
    The Sahel region typically experiences a single rainy season, with the rest of the year being very dry.
    Temperature patterns often show inverse relationships with rainfall.
    """)

elif chart_type == "Monthly Comparison":
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_monthly_comparison_chart(
                df, selected_temp_var, WEATHER_VARIABLES[selected_temp_var]
            ),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            create_monthly_comparison_chart(
                df, selected_precip_var, WEATHER_VARIABLES[selected_precip_var]
            ),
            use_container_width=True,
        )

    st.markdown("""
    These charts allow you to compare monthly patterns across different years.
    You can observe how weather variables change from month to month and identify
    any year-to-year variations or trends.
    """)

elif chart_type == "Seasonal Patterns":
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_seasonal_heatmap(
                df, selected_temp_var, WEATHER_VARIABLES[selected_temp_var]
            ),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            create_seasonal_heatmap(
                df, selected_precip_var, WEATHER_VARIABLES[selected_precip_var]
            ),
            use_container_width=True,
        )

    st.markdown("""
    The heatmaps visualize seasonal patterns across years, making it easy to identify
    months with extreme values and compare patterns between years. Darker colors represent
    higher values for the selected variables.
    """)

elif chart_type == "Annual Cycle":
    st.plotly_chart(
        create_annual_cycle_chart(
            df, selected_temp_var, WEATHER_VARIABLES[selected_temp_var]
        ),
        use_container_width=True,
    )

    st.markdown("""
    The annual cycle chart displays weather patterns throughout the year in a circular format,
    emphasizing the cyclical nature of seasonal changes. Each line represents a different year,
    allowing for easy comparison of annual patterns.
    """)

elif chart_type == "Statistical Distribution":
    st.plotly_chart(
        create_yearly_comparison_boxplot(
            df, selected_temp_var, WEATHER_VARIABLES[selected_temp_var]
        ),
        use_container_width=True,
    )

    st.markdown("""
    Boxplots show the statistical distribution of weather variables by month across different years.
    They display the median, quartiles, and range of values, helping identify the variability and
    extremes in the data.
    """)

elif chart_type == "Wind Patterns":
    st.plotly_chart(create_wind_rose_chart(df), use_container_width=True)

    st.markdown("""
    The wind rose chart shows the distribution of wind speeds throughout the year.
    The Sahel region often experiences the Harmattan, a dry and dusty trade wind that
    blows from the northeast across the region during the dry season.
    """)

# Show data attribution
st.caption(
    "Data Source: Historical weather data from Open-Meteo Archive API (https://open-meteo.com/)"
)

# Expandable raw data view
with st.expander("View raw data"):
    st.dataframe(df)

# Information about the Sahel region
st.markdown("---")
sahel_info = get_sahel_info()

st.markdown(f"### {sahel_info['title']}")
st.markdown(sahel_info["description"])

st.markdown("#### Key Climate Features")
for feature in sahel_info["climate_features"]:
    st.markdown(f"- {feature}")