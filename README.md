# START Hack 2025 - Team "LONIGO MAGGIORE DI BRENTA ARZICHIAMPO"

This project was developed during **START Hack 2025**, Europe’s most entrepreneurial 36-hour hackathon, held in St. Gallen, Switzerland.

## Context and Goals

The challenge was to support the **United Nations Convention to Combat Desertification (UNCCCD)** as part of their key initiative—the G20 Global Land Initiative. Our focus was to raise awareness about the severe environmental and socio-economic challenges faced by the Sahel region.

## What We Did

We developed an interactive web app that:

- **Collects and visualizes historical data:** Displays 20 years of data on precipitation, land cover, and population density in the Sahel.
- **Integrates future projections using ML:** Provides forecasts for the next 10 years to highlight potential trends.
- **Offers interactive support:** Includes a chatbot that answers users' questions and helps navigate the information.

## Repository Structure

- **Local Testing:**
  To run the app locally, execute:
  ```bash
  cd website
  uv run streamlit run 1_Home_Page.py
  ```
- **README_DATASET:**  
  This file contains a summary explaining what each feature in the datasets represents.

- **UserGuide:**  
  This folder contains the complete user guide.

- **Dataset:**
  - **original:** Contains the original dataset in `.tif` format.
  - **csv:** Contains the dataset converted to `.csv` format for easier readability.
