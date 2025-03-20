import streamlit as st
from config import configure_page
from sidebar import sidebar_controls
from charts import display_chart
from utils import get_historical_weather_data, get_sahel_info

# Configurare la pagina
configure_page()

# Titolo e descrizione
st.title("🏜️ Sahel Desert Weather Visualization")
st.markdown("""
    Explore the weather patterns of the Sahel desert region through interactive visualizations.
    This dashboard provides insights into temperature, precipitation, humidity, and wind patterns
    throughout the year across multiple locations in the Sahel.
""")

# Sidebar
selected_location, start_year, end_year, selected_temp_var, selected_precip_var, chart_type = sidebar_controls()

# Caricare i dati
with st.spinner("Fetching weather data for the Sahel region..."):
    df = get_historical_weather_data(selected_location, start_year, end_year)

if df is not None:
    st.markdown(f"### Weather data for {selected_location} ({start_year}-{end_year})")

    # Mostrare il grafico selezionato
    display_chart(chart_type, df, selected_temp_var, selected_precip_var)

    # Mostrare i dati grezzi
    with st.expander("View raw data"):
        st.dataframe(df)

    # Informazioni sulla regione del Sahel
    st.markdown("---")
    sahel_info = get_sahel_info()
    st.markdown(f"### {sahel_info['title']}")
    st.markdown(sahel_info["description"])
    st.markdown("#### Key Climate Features")
    for feature in sahel_info["climate_features"]:
        st.markdown(f"- {feature}")

else:
    st.error("Failed to load weather data. Please try a different location or time period.")
