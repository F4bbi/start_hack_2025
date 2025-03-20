import streamlit as st
import plotly.express as px
import pandas as pd
from data_processor import (
    create_annual_cycle_chart,
    create_combined_chart,
    create_monthly_comparison_chart,
    create_seasonal_heatmap,
    create_wind_rose_chart,
    create_yearly_comparison_boxplot,
)

def display_chart(chart_type, df, selected_temp_var, selected_precip_var):
    if chart_type == "Temperature & Precipitation":
        uploaded_file = st.file_uploader("Carica un file CSV", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            fig = px.scatter(
                df,
                x="lon",
                y="lat",
                color="precipitation",
                color_continuous_scale="viridis",
            )
            fig.update_layout(
                height=600,
                xaxis=dict(scaleanchor="y", visible=False),
                yaxis=dict(visible=False),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Monthly Comparison":
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                create_monthly_comparison_chart(df, selected_temp_var, selected_temp_var),
                use_container_width=True,
            )
        with col2:
            st.plotly_chart(
                create_monthly_comparison_chart(df, selected_precip_var, selected_precip_var),
                use_container_width=True,
            )

    elif chart_type == "Seasonal Patterns":
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                create_seasonal_heatmap(df, selected_temp_var, selected_temp_var),
                use_container_width=True,
            )
        with col2:
            st.plotly_chart(
                create_seasonal_heatmap(df, selected_precip_var, selected_precip_var),
                use_container_width=True,
            )

    elif chart_type == "Annual Cycle":
        st.plotly_chart(
            create_annual_cycle_chart(df, selected_temp_var, selected_temp_var),
            use_container_width=True,
        )

    elif chart_type == "Statistical Distribution":
        st.plotly_chart(
            create_yearly_comparison_boxplot(df, selected_temp_var, selected_temp_var),
            use_container_width=True,
        )

    elif chart_type == "Wind Patterns":
        st.plotly_chart(create_wind_rose_chart(df), use_container_width=True)
