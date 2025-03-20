import streamlit as st
from openai import OpenAI

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
    value=2023 if 2023 in years else 2020,
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


def ai_chat():
    AI_API_ENDPOINT = st.secrets["AI_API_ENDPOINT"]
    AI_API_TOKEN = st.secrets["AI_API_TOKEN"]
    SYSTEM_PROMPT = """\
You are an expert from the G20 Global Land Initiative led by the United Nations Convention to Combat Desertification (UNCCD).
Your role is to provide data-driven answers, insights, and recommendations based mainly on the data I will give you, and also on the public available data about Sahel desert.
You must only answer questions about the Sahel desert region in Africa. Be concise. Avoid mentioning the source you used.

Datatypes about the last 20 years of the Sahel region. We are in 2023, data after 2023 is a prediction.
Each value at position `n` corresponds to the year in position `n` of the current datatype.
<datatype>
name: population_density
year: [2010, 2015, 2020, 2025, 2030, 2035]
min: [0, 0, 0, 0, 0, 0]
max: [1225, 1224, 1802, 1832, 2409, 2439]
mean: [8, 9, 10, 11, 12, 12]
std: [26, 27, 36, 37, 45, 46]
</datatype>
<datatype>
name: gross_primary
year: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
min: [266, 199, 370, 306, 272, 212, 316, 171, 231, 203, 307, 178, 229, 233]
max: [65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533]
mean: [24423, 23966, 24425, 24136, 24054, 24145, 24458, 23890, 24068, 24053, 24456, 23944, 24722, 24178]
std: [30675, 31013, 30671, 30886, 30948, 30880, 30648, 31069, 30938, 30949, 30651, 31030, 30453, 30856]
</datatype>
<datatype>
name: climate_precipitation
year: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040]
min: [85, 41, 55, 54, 40, 49, 57, 45, 51, 37, 53, 42, 58, 52, 47, 0, 44, 48, 55, 48, 55, 21, 50, 50, 50, 48, 49, 35, 50, 47, 53]
max: [500, 367, 609, 484, 440, 500, 578, 415, 542, 442, 690, 441, 566, 511, 626, 460, 573, 542, 599, 487, 566, 544, 568, 514, 568, 531, 543, 534, 569, 518, 531]
mean: [358, 200, 351, 261, 236, 245, 295, 226, 256, 187, 354, 227, 315, 249, 324, 252, 303, 266, 310, 261, 301, 274, 299, 270, 297, 277, 295, 274, 295, 279, 292]
std: [103, 76, 136, 97, 103, 101, 115, 91, 109, 88, 160, 90, 148, 103, 155, 100, 144, 115, 142, 109, 140, 119, 137, 115, 137, 120, 133, 119, 135, 121, 131]
</datatype>"""

    client = OpenAI(base_url=AI_API_ENDPOINT, api_key=AI_API_TOKEN)

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # st.session_state.messages = []

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖Chat with AI")

    chat_container = st.sidebar.container()

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue

        with chat_container.chat_message(message["role"]):
            chat_container.markdown(message["content"])

    if prompt := chat_container.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with chat_container.chat_message("user"):
            chat_container.markdown(prompt)

        with chat_container.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="mixtral",
                # model="mixtral8x22b",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = chat_container.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()


ai_chat()
