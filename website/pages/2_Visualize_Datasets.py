import streamlit as st

from utils import BASE_DATA_FOLDER, DATA_LIST, create_chart, plot

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
    "Select year",
    min_value=int(years[0]),
    max_value=int(years[-1]),
    value=2023 if 2023 in years else years[0],
    step=years[1] - years[0],
)

# Download button
st.sidebar.download_button(
    label="Download CSV",
    data=files[0].read_bytes(),
    file_name=f"{selected_location[0]}-{year}.csv",
    mime="text/csv",
)

col1, col2 = st.columns([0.7, 2])

with col1:
    st.markdown(f"### {selected_location[1]['name']} for year {year}")

with col2:
    if year >= 2024:
        st.warning("⚠️ This is a prediction based on historical data.")

# Display selected chart based on user choice
for file in files:
    if f"{str(file.parent.name)}-{file.name}" not in st.session_state:
        st.session_state[f"{str(file.parent.name)}-{file.name}"] = create_chart(file)

# Display the chart
plot(st.session_state[f"{selected_location[0]}-{year}.csv"])
