import streamlit as st

from utils import BASE_DATA_FOLDER, DATA_LIST, create_chart, plot

st.set_page_config(
    page_title="Sahel Correlation Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Correlation Analysis in Sahel")
st.markdown("""
    Explore correlations between different climate and environmental variables in the Sahel region.
    Select two datasets to compare and analyze the relationships between them.
""")

st.sidebar.title("Settings")

location1 = st.sidebar.selectbox(
    "Select the first data you want to see",
    options=list(DATA_LIST.items()),
    index=0,
    format_func=lambda x: x[1]["name"],
)

files1 = [
    file.resolve()
    for file in (BASE_DATA_FOLDER / location1[0]).iterdir()
    if file.is_file()
]

years1 = sorted(
    {
        int(file.name.split("_")[-1].split(".")[0])
        for file in files1
        if file.name.endswith(".csv")
    }
)

year1 = st.sidebar.slider(
    "Select year",
    key="year1",
    min_value=int(years1[0]),
    max_value=int(years1[-1]),
    value=2023 if 2023 in years1 else 2020,
    step=years1[1] - years1[0],
)

location2 = st.sidebar.selectbox(
    "Select the second data you want to see",
    options=list(DATA_LIST.items()),
    index=1,
    format_func=lambda x: x[1]["name"],
)

files2 = [
    file.resolve()
    for file in (BASE_DATA_FOLDER / location2[0]).iterdir()
    if file.is_file()
]

years2 = sorted(
    {
        int(file.name.split("_")[-1].split(".")[0])
        for file in files2
        if file.name.endswith(".csv")
    }
)

year2 = st.sidebar.slider(
    "Select year",
    key="year2",
    min_value=int(years2[0]),
    max_value=int(years2[-1]),
    value=2023 if 2023 in years2 else 2020,
    step=years2[1] - years2[0],
)

file1 = f"{location1[0]}/{year1}.csv"
file2 = f"{location2[0]}/{year2}.csv"

if file1 not in st.session_state:
    st.session_state[file1] = create_chart(BASE_DATA_FOLDER / file1)
if file2 not in st.session_state:
    st.session_state[file2] = create_chart(BASE_DATA_FOLDER / file2)

st.markdown(
    f"### Correlation between {location1[1]['name']} and {location2[1]['name']} for years {year1} and {year2}"
)

col1, col2 = st.columns(2)

with col1:
    if year1 >= 2024:
        st.warning("⚠️ This is a prediction based on historical data.")

with col2:
    if year2 >= 2024:
        st.warning("⚠️ This is a prediction based on historical data.")

col1, col2 = st.columns(2)

with col1:
    plot(st.session_state[file1], "plot1")
with col2:
    plot(st.session_state[file2], "plot2")

st.divider()
