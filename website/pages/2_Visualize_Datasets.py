import streamlit as st
#from openai import OpenAI

from utils import BASE_DATA_FOLDER, DATA_LIST, create_chart, plot

# configure page
st.set_page_config(
    page_title="START Hack 2025 - Innovating for Land Restoration",
    page_icon="🏜️",
    layout="wide",
    initial_sidebar_state="expanded",
)

page = {
    "🌧️ Precipitation": {
        "name": "precipitation",
        "upper_name": "Precipitation",
        "timelapse": "static/videos/timelapse_precipitazioni.mp4",
        "start_date": "2010",
        "end_date": "2040",
        "insights": """
        In 2010, rainfall levels were notably high throughout the year, marking an exceptional period of precipitation. However, in the subsequent years, precipitation levels stabilized, showing a relatively consistent pattern up to the present day.

        A geographical disparity is also evident in the distribution of rainfall. The southern areas of the Sahel have consistently received moderate to substantial rainfall, supporting local ecosystems and agriculture. In contrast, the northern parts of the region have experienced minimal precipitation, reinforcing the prevailing arid conditions characteristic of the area.

        These trends highlight the persistent climatic challenges in the region and underline the importance of sustainable water resource management strategies to mitigate the effects of prolonged dry conditions in northern areas while optimizing agricultural potential in the south.
    """,
    },
    "⛽️ Gross Primary Production": {
        "name": "gross primary production",
        "upper_name": "Gross Primary Production",
        "timelapse": "static/videos/timelapse_gross.mp4",
        "start_date": "2010",
        "end_date": "2023",
        "insights": """
The analysis of gross primary production (GPP) in the Sahel region over time indicates a remarkable consistency, with little variation across the years. This stability suggests that the region's overall capacity for biomass production has remained largely unchanged despite environmental and socio-economic developments.

However, significant geographical differences are evident. The central and southern areas of the region consistently exhibit lower GPP values, reflecting the arid and semi-arid conditions that limit vegetation growth. In contrast, the northwestern areas show notably high levels of primary production, exceeding 60,000 kg_C/m²/year. This disparity may be attributed to localized climatic and ecological factors, such as variations in soil fertility, water availability, and vegetation density.

One possible explanation for the overall stability of GPP is the relatively slow population growth in the Sahel, which has resulted in minimal changes in land use and resource exploitation. Additionally, the persistence of the region's natural flora, particularly in the northwestern zones, has likely played a key role in maintaining high production levels in certain areas. Unlike regions undergoing rapid deforestation or agricultural expansion, the Sahel's vegetation cover has remained relatively stable, supporting a consistent level of biomass production.

This pattern underscores the resilience of the region's natural productivity but also highlights critical challenges. The lower GPP in the central and southern areas suggests limited agricultural potential, which could affect food security and economic development. Meanwhile, the high production levels in the northwest present opportunities for sustainable resource management, provided that environmental balance is maintained.
                        """,
    },
    "🌿 Land Cover": {
        "name": "land cover",
        "upper_name": "Land Cover",
        "timelapse": "static/videos/timelapse_land.mp4",
        "start_date": "2010",
        "end_date": "2023",
        "insights": """
The analysis of land cover in the Sahel region over time reveals a largely stable distribution of ecosystem types, with minimal overall change. The northern areas remain predominantly barren, characterized by arid and desert landscapes with little to no vegetation. In contrast, the central and southern regions are consistently dominated by grasslands, which form the primary vegetation cover across most of the area.

Despite this general stability, some localized variations have been observed. Open shrublands appear intermittently, fluctuating over time without establishing a long-term presence in any specific area. This variability may be influenced by periodic climatic shifts, grazing pressure, or small-scale land use changes.

Urban land and croplands, while present, remain exceptionally rare. Only a few scattered points of human settlement and agricultural development have been detected, indicating that large-scale urbanization and intensive farming have not yet significantly altered the Sahel’s landscape. The scarcity of these land cover types suggests that the region remains largely shaped by natural processes rather than extensive human intervention.

Overall, the stability of land cover in the Sahel highlights the resilience of its ecosystems but also underscores the challenges of development in the region. The persistence of barren land in the north and the predominance of grasslands elsewhere suggest limited opportunities for large-scale agricultural expansion. However, the sporadic emergence of shrublands and the rare presence of croplands may indicate potential areas where land use could evolve in response to environmental or socio-economic changes.
                      """,
    },
    "🧍🏻 Population Density": {
        "name": "population density",
        "upper_name": "Population Density",
        "timelapse": "static/videos/timelapse_population.mp4",
        "start_date": "2010",
        "end_date": "2035",
        "insights": """
The population density in the Sahel region remains exceptionally low, with an average of only 8 inhabitants per square kilometer across the entire area. However, there is a notable concentration of population in the central region, where densities range between 1,000 and 2,000 inhabitants per square kilometer. This pattern suggests that certain environmental factors—potentially a balance between sufficient rainfall and manageable aridity—make this area more suitable for human settlement compared to the harsher conditions of the surrounding regions.

Despite the overall low population density, a gradual increase has been observed over the years. While this growth remains moderate, it reflects a slow but steady demographic expansion, likely influenced by improved living conditions, migration patterns, or slight changes in land use.

The persistence of low population density across most of the Sahel highlights the region’s challenging living conditions, including water scarcity, limited agricultural potential, and extreme climatic variability. The central concentration of inhabitants may indicate pockets of greater environmental suitability, where conditions allow for more sustainable livelihoods. However, the slow growth trend suggests that large-scale urbanization or intensive land use transformation remains unlikely in the near future.

Understanding these dynamics is crucial for planning sustainable development strategies, ensuring that resources are allocated effectively while preserving the delicate ecological balance of the region.
                                """,
    },
}

# Sidebar
st.sidebar.title("Settings")

# Location selection
selected_location = st.sidebar.selectbox(
    "Select data you want to see",
    options=list(DATA_LIST.items()),
    index=0,
    format_func=lambda x: x[1]["name"],
)

choice = selected_location[1]["name"]

# Dynamic title and subtitle
page_title = choice
page_section = page[choice]["name"]
page_subtitle = f"In this page, you can visualize the data about {page_section} for the Sahel region in Africa.\
    The data is based on historical records and predictions for the future. Below you can also see some data analysis and insights based on the {page_section} data, \
    and if you want you can download the data as a CSV file and use it for your analysis."

# Display updated title and subtitle
st.title(page_title)
st.markdown(page_subtitle)

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

if year >= 2024:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"### {page[choice]['upper_name']} for year {year}")

    with col2:
        st.warning("⚠️ This is a prediction based on historical data.")
else:
    st.markdown(f"### {page[choice]['upper_name']} for year {year}")

# Display selected chart based on user choice
for file in files:
    if f"{str(file.parent.name)}-{file.name}" not in st.session_state:
        st.session_state[f"{str(file.parent.name)}-{file.name}"] = create_chart(file)

# Display the chart
plot(st.session_state[f"{selected_location[0]}-{year}.csv"])

st.markdown("## ⏳ Timelapse of the data")
video_file = open(page[choice]["timelapse"], "rb")
video_bytes = video_file.read()
st.markdown(
    f"In this section you can see a timelapse of the {page[choice]['name']} data from {page[choice]['start_date']} to {page[choice]['end_date']}."
)
st.video(video_bytes)

st.markdown("## 🔎 Insights & Analysis based on the data")
st.markdown(page[choice]["insights"])


# def ai_chat():
#     AI_API_ENDPOINT = st.secrets["AI_API_ENDPOINT"]
#     AI_API_TOKEN = st.secrets["AI_API_TOKEN"]
#     SYSTEM_PROMPT = """\
# You are an expert from the G20 Global Land Initiative led by the United Nations Convention to Combat Desertification (UNCCD).
# Your role is to provide data-driven answers, insights, and recommendations based mainly on the data I will give you, and also on the public available data about Sahel desert.
# You must only answer questions about the Sahel desert region in Africa. Be concise. Avoid mentioning the source you used.

# Datatypes about the last 20 years of the Sahel region. We are in 2023, data after 2023 is a prediction.
# Each value at position `n` corresponds to the year in position `n` of the current datatype.
# <datatype>
# name: population_density
# year: [2010, 2015, 2020, 2025, 2030, 2035]
# min: [0, 0, 0, 0, 0, 0]
# max: [1225, 1224, 1802, 1832, 2409, 2439]
# mean: [8, 9, 10, 11, 12, 12]
# std: [26, 27, 36, 37, 45, 46]
# </datatype>
# <datatype>
# name: gross_primary
# year: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
# min: [266, 199, 370, 306, 272, 212, 316, 171, 231, 203, 307, 178, 229, 233]
# max: [65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533, 65533]
# mean: [24423, 23966, 24425, 24136, 24054, 24145, 24458, 23890, 24068, 24053, 24456, 23944, 24722, 24178]
# std: [30675, 31013, 30671, 30886, 30948, 30880, 30648, 31069, 30938, 30949, 30651, 31030, 30453, 30856]
# </datatype>
# <datatype>
# name: climate_precipitation
# year: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040]
# min: [85, 41, 55, 54, 40, 49, 57, 45, 51, 37, 53, 42, 58, 52, 47, 0, 44, 48, 55, 48, 55, 21, 50, 50, 50, 48, 49, 35, 50, 47, 53]
# max: [500, 367, 609, 484, 440, 500, 578, 415, 542, 442, 690, 441, 566, 511, 626, 460, 573, 542, 599, 487, 566, 544, 568, 514, 568, 531, 543, 534, 569, 518, 531]
# mean: [358, 200, 351, 261, 236, 245, 295, 226, 256, 187, 354, 227, 315, 249, 324, 252, 303, 266, 310, 261, 301, 274, 299, 270, 297, 277, 295, 274, 295, 279, 292]
# std: [103, 76, 136, 97, 103, 101, 115, 91, 109, 88, 160, 90, 148, 103, 155, 100, 144, 115, 142, 109, 140, 119, 137, 115, 137, 120, 133, 119, 135, 121, 131]
# </datatype>"""

#     client = OpenAI(base_url=AI_API_ENDPOINT, api_key=AI_API_TOKEN)

#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#         # st.session_state.messages = []

#     st.sidebar.markdown("---")
#     st.sidebar.markdown("### 🤖Chat with AI")

#     chat_container = st.sidebar.container()

#     for message in st.session_state.messages:
#         if message["role"] == "system":
#             continue

#         with chat_container.chat_message(message["role"]):
#             chat_container.markdown(message["content"])

#     if prompt := chat_container.chat_input("What is up?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         with chat_container.chat_message("user"):
#             chat_container.markdown(prompt)

#         with chat_container.chat_message("assistant"):
#             stream = client.chat.completions.create(
#                 model="mixtral",
#                 # model="mixtral8x22b",
#                 messages=[
#                     {"role": m["role"], "content": m["content"]}
#                     for m in st.session_state.messages
#                 ],
#                 stream=True,
#             )
#             response = chat_container.write_stream(stream)

#         st.session_state.messages.append({"role": "assistant", "content": response})

#         st.rerun()

def poor_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖Chat with AI")

    chat_container = st.sidebar.container()

    for message in st.session_state.messages:
        with chat_container.chat_message(message["role"]):
            chat_container.markdown(message["content"])

    if prompt := chat_container.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with chat_container.chat_message("user"):
            chat_container.markdown(prompt)

        with chat_container.chat_message("assistant"):
            response = "Sorry, but the owner of this project does not have the money to pay for the LLMs API. \
            Imagine that this is a nice and clear answer for your question about the G20 Global Land Initiative. 😊"
            chat_container.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()


#ai_chat()
poor_chat()