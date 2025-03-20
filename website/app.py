import pandas as pd
import plotly.express as px
import streamlit as st

from pathlib import Path

from utils import DATA_LIST

BASE_DATA_FOLDER = Path("../dataset/csv/")


def create_chart(file):
    df = pd.read_csv(file)

    fig = px.scatter(
        df,
        x="lon",
        y="lat",
        color="value",
        color_continuous_scale="viridis",
    )
    fig.update_layout(
        height=600,
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


# Configure page
st.set_page_config(
    page_title="Sahel Desert Visualizer",
    page_icon="🏜️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("🏜️ Sahel Desert Visualizer")
st.markdown("""
    Explore the weather patterns of the Sahel desert region through interactive visualizations.
    This dashboard provides insights into temperature, precipitation, humidity, and wind patterns
    throughout the year across multiple locations in the Sahel.
""")

# Sidebar
st.sidebar.title("Settings")

# Location selection
selected_location = st.sidebar.selectbox(
    "Select data you want to see",
    options=list(DATA_LIST.items()),
    index=0,
    format_func=lambda x: x[1]["name"],
)

files = [
    file.resolve()
    for file in (BASE_DATA_FOLDER / selected_location[0]).iterdir()
    if file.is_file()
]

years = sorted(
    {
        int(file.name.split("_")[-1].split(".")[0])
        for file in files
        if file.name.endswith(".csv")
    }
)


# Year range
year = st.sidebar.slider(
    "Select year range",
    min_value=int(years[0]),
    max_value=int(years[-1]),
    value=int(years[0]),
    step=years[1] - years[0],
)

# Show basic info about the data
st.markdown(f"### {selected_location[1]['name']} for year {year}")

# Display selected chart based on user choice
for file in files:
    if f"{str(file.parent.name)}-{file.name}" not in st.session_state:
        st.session_state[f"{str(file.parent.name)}-{file.name}"] = create_chart(
            str(file)
        )

# Display the chart
plot(st.session_state[f"{selected_location[0]}-{year}.csv"])

st.markdown("""
This chart shows the relationship between temperature and precipitation throughout the year.
The Sahel region typically experiences a single rainy season, with the rest of the year being very dry.
Temperature patterns often show inverse relationships with rainfall.
""")
