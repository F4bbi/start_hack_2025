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
    options=[item for item in DATA_LIST.items() if item != location1],
    index=0,
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

correlations = {
    "climate_precipitation-gross_primary": """
        The main correlation is that areas with higher precipitation tend to coincide with regions with greater Gross Primary Production (GPP). This is logical since water is a fundamental limiting factor for photosynthesis and plant growth.  

        ### More specifically:

        - Areas with higher precipitation values (yellow) tend to correspond to yellow regions in the GPP graph, indicating higher primary production.  
        - Areas with lower precipitation values (purple) tend to correspond to purple regions in the GPP graph, indicating lower primary production.

        ### Additional considerations:

        - **Other factors:** Besides precipitation, other factors can influence GPP, such as temperature, solar radiation, nutrient availability, and the type of vegetation present.  
        - **Non-linear relationship:** The relationship between precipitation and GPP may not be linear. In some areas, an increase in precipitation might not result in a proportional increase in GPP due to other limiting factors.  
        - **Spatial scale:** The observed correlation is at a regional scale. At more local scales, the relationship may be more complex and influenced by site-specific factors.
    """,
    "climate_precipitation-land_cover": """
        A key correlation we can observe is that areas with higher precipitation tend to coincide with regions rich in vegetation, such as grasslands and cultivated fields. Conversely, areas with lower precipitation are more likely to have arid land cover or open shrublands.

        ### More specifically:

        - Areas with higher precipitation values (yellow) tend to correspond to green regions in the land cover graph, indicating the presence of grasslands and cultivated fields.  
        - Areas with lower precipitation values (purple) tend to correspond to brown regions in the land cover graph, indicating the presence of arid lands.
    """,
    "climate_precipitation-population_density": """
        The main correlation is that areas with higher precipitation tend to have higher population density, though there are exceptions. This aligns with the fact that water is an essential resource for human settlement and agricultural activities.  

        ### However, the relationship is not as straightforward as in previous cases. Specifically:

        - **Population "hotspots"** can be observed even in areas where precipitation is not the highest. This may be due to several factors, such as:  
        - **Urban centers:** Cities attract populations regardless of precipitation levels, driven by economic, social, and service-related factors.  
        - **Alternative water sources:** The presence of rivers, lakes, or underground aquifers can compensate for low precipitation.  
        - **Specific economic activities:** Mining, industrial, or commercial activities can attract populations even in areas with scarce precipitation.  

        - The area with the highest precipitation, in the upper part of the map, does not seem to have a population density proportional to the amount of rainfall. This could be due to factors such as soil quality, the presence of diseases, or even cultural influences.
    """,
    "gross_primary-land_cover": """
        The main correlation is that areas with high Gross Primary Production (GPP) (yellow) primarily correspond to regions with grassland cover (green). Conversely, areas with low GPP (purple) are more associated with arid lands (light brown) and open shrublands.  

        ### More specifically:

        - The yellow area in the north of the GPP graph primarily corresponds to the green area (grasslands) in the land cover graph. This indicates that grasslands are highly productive in terms of biomass.  
        - The purple area in the south of the GPP graph mainly corresponds to the light brown (arid) and open shrubland areas in the land cover graph. This suggests that arid lands and open shrublands have low primary productivity.  

        ### Additional considerations:

        - **Grassland type:** It would be useful to determine the specific type of grassland present, as some types may be more productive than others.  
        - **Limiting factors:** GPP is influenced by several factors, including the availability of water, nutrients, and sunlight. The observed correlation suggests that water is a crucial limiting factor for GPP in this region, as areas with greater grassland cover (which require more water) exhibit higher GPP.  
        - **Human activities:** The presence of croplands may influence GPP in certain areas, although this is not clearly visible in this analysis.
    """,
    "gross_primary-population_density": """
        The correlation between Gross Primary Production (GPP) and population density is complex and non-linear.  

        ### Key Insights:

        - **Influence of GPP:** Areas with relatively high GPP tend to support higher population densities, especially in agricultural regions. Many population hotspots align with zones of elevated GPP.  
        - **Alternative Factors:** Population density is shaped by various factors beyond GPP, including:  
        - **Urbanization:** Cities attract people due to economic opportunities and infrastructure, even in areas with low GPP.  
        - **Water resources:** Rivers and aquifers can sustain populations where GPP is low.  
        - **Economic activities:** Mining, industry, and commerce create population clusters in low-productivity areas.  
        - **Historical and cultural factors:** Settlement history and traditions influence population distribution.  

        ### Conclusion:

        While GPP plays a role in shaping population density, it is just one of many interacting environmental, economic, and social factors.
    """,
    "land_cover-population_density": """
        The main correlation is that areas with a higher presence of grasslands with annual grasses (green) tend to have higher population density, though with notable exceptions. This suggests that even non-grassland areas can provide resources valuable for human settlement.  

        ### Key Insights:

        - **Grasslands and population:** The green areas (grasslands) in the land cover graph generally show higher population density, likely due to their suitability for grazing or resource gathering.  
        - **Exceptions and alternative factors:** Population "hotspots" also appear in arid land areas (light brown), indicating that factors such as urban centers, alternative water sources, or specific economic activities can drive population density regardless of land cover type.  

        ### Conclusion:

        While land cover influences population distribution, other factors like economic opportunities, infrastructure, and water availability play a crucial role in shaping settlement patterns.
    """,
}

correlation_key = (
    f"{location1[0]}-{location2[0]}"
    if location1[0] < location2[0]
    else f"{location2[0]}-{location1[0]}"
)
if correlation_key in correlations:
    st.markdown("## 🔎 Insights & Analysis")
    st.markdown(correlations[correlation_key])

st.divider()
