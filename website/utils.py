import pandas as pd
import requests
import streamlit as st

# Coordinates for various locations in the Sahel region
SAHEL_LOCATIONS = {
    "Dakar, Senegal": {"lat": 14.7167, "lon": -17.4677},
    "Bamako, Mali": {"lat": 12.6392, "lon": -8.0029},
    "Niamey, Niger": {"lat": 13.5137, "lon": 2.1098},
    "Khartoum, Sudan": {"lat": 15.5007, "lon": 32.5599},
    "N'Djamena, Chad": {"lat": 12.1348, "lon": 15.0557},
}

# Weather variables and their user-friendly names
WEATHER_VARIABLES = {
    "temperature_2m_max": "Maximum Temperature (°C)",
    "temperature_2m_min": "Minimum Temperature (°C)",
    "temperature_2m_mean": "Mean Temperature (°C)",
    "precipitation_sum": "Precipitation (mm)",
    "rain_sum": "Rainfall (mm)",
    "relative_humidity_2m_mean": "Relative Humidity (%)",
    "wind_speed_10m_max": "Maximum Wind Speed (km/h)",
    "wind_gusts_10m_max": "Maximum Wind Gusts (km/h)",
}


def get_historical_weather_data(location, start_year=2020, end_year=2023):
    """
    Fetch historical weather data for a location in the Sahel region
    """
    lat, lon = SAHEL_LOCATIONS[location]["lat"], SAHEL_LOCATIONS[location]["lon"]

    # Create date ranges for each year
    all_data = []

    for year in range(start_year, end_year + 1):
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,rain_sum,relative_humidity_2m_mean,wind_speed_10m_max,wind_gusts_10m_max&timezone=GMT"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
            data = response.json()

            if "daily" in data:
                df = pd.DataFrame(data["daily"])
                df["year"] = year
                all_data.append(df)
            else:
                st.error(
                    f"No data available for {location} in {year}. Response: {data}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data for {location} in {year}: {str(e)}")
            continue

    if not all_data:
        return None

    # Combine all years of data
    combined_df = pd.concat(all_data, ignore_index=True)

    # Convert time column to datetime
    combined_df["time"] = pd.to_datetime(combined_df["time"])

    # Extract month and day for seasonal analysis
    combined_df["month"] = combined_df["time"].dt.month
    combined_df["day"] = combined_df["time"].dt.day
    combined_df["month_name"] = combined_df["time"].dt.month_name()

    return combined_df


def get_sahel_info():
    """
    Returns information about the Sahel region
    """
    return {
        "title": "The Sahel Desert",
        "description": """
        The Sahel is a semi-arid region of western and north-central Africa extending from Senegal to Sudan. 
        It forms a transitional zone between the arid Sahara Desert to the north and the more humid savanna 
        belt to the south. The Sahel spans approximately 5,400 km from the Atlantic Ocean in the west to the 
        Red Sea in the east, with a width varying from several hundred to a thousand kilometers.

        The region's climate is characterized by a short rainy season (typically June to September) followed 
        by a longer dry season. Annual rainfall ranges from 200-600mm, and temperatures can reach extremes, 
        with daily maximums often exceeding 40°C (104°F) during the hottest months.

        The Sahel is particularly vulnerable to climate change and has experienced significant droughts and 
        periods of desertification throughout its recent history.
        """,
        "climate_features": [
            "Distinct wet and dry seasons",
            "High temperature variability throughout the year",
            "Prone to prolonged droughts",
            "Increasing rainfall variability due to climate change",
            "Seasonal Harmattan winds (dry, dusty winds from the northeast)",
        ],
    }
