import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def prepare_monthly_averages(df, variable):
    """
    Prepare monthly averages for a given weather variable
    """
    # Group by month and calculate averages for each year
    monthly_data = (
        df.groupby(["year", "month", "month_name"])[variable].mean().reset_index()
    )

    # Sort by month for proper x-axis ordering
    monthly_data["month_name"] = pd.Categorical(
        monthly_data["month_name"],
        categories=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        ordered=True,
    )
    monthly_data = monthly_data.sort_values(["year", "month_name"])

    return monthly_data


def create_monthly_comparison_chart(df, variable, variable_name):
    """
    Create a monthly comparison chart for different years
    """
    monthly_data = prepare_monthly_averages(df, variable)

    fig = px.line(
        monthly_data,
        x="month_name",
        y=variable,
        color="year",
        markers=True,
        title=f"Monthly {variable_name} in the Sahel Region",
        labels={"month_name": "Month", variable: variable_name, "year": "Year"},
        color_discrete_sequence=px.colors.qualitative.Safe,
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title=variable_name,
        legend_title="Year",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig


def create_seasonal_heatmap(df, variable, variable_name):
    """
    Create a heatmap showing seasonal patterns
    """
    # Group by month and year
    pivot_data = df.pivot_table(
        index="month_name", columns="year", values=variable, aggfunc="mean"
    )

    # Reorder months
    pivot_data = pivot_data.reindex(
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
    )

    # Create heatmap
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Year", y="Month", color=variable_name),
        x=pivot_data.columns,
        y=pivot_data.index,
        color_continuous_scale="YlOrRd" if "temp" in variable.lower() else "Blues",
        title=f"Seasonal {variable_name} Patterns by Year",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0), coloraxis_colorbar=dict(title=variable_name)
    )

    return fig


def create_yearly_comparison_boxplot(df, variable, variable_name):
    """
    Create a boxplot comparing yearly distributions
    """
    fig = px.box(
        df,
        x="month_name",
        y=variable,
        color="year",
        title=f"Monthly Distribution of {variable_name} by Year",
        labels={"month_name": "Month", variable: variable_name, "year": "Year"},
        color_discrete_sequence=px.colors.qualitative.Safe,
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title=variable_name,
        legend_title="Year",
        boxmode="group",
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig


def create_annual_cycle_chart(df, variable, variable_name):
    """
    Create a radial chart showing the annual cycle of a weather variable
    """

    # Create the radial chart
    fig = go.Figure()

    for year in df["year"].unique():
        year_data = prepare_monthly_averages(df[df["year"] == year], variable)

        fig.add_trace(
            go.Scatterpolar(
                r=year_data[variable],
                theta=year_data["month_name"],
                name=str(year),
                mode="lines+markers",
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, title=variable_name),
            angularaxis=dict(
                categoryarray=[
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ]
            ),
        ),
        title=f"Annual Cycle of {variable_name}",
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig


def create_combined_chart(df, temp_var, precip_var):
    """
    Create a combined chart showing temperature and precipitation
    """
    monthly_temp = prepare_monthly_averages(df, temp_var)
    monthly_precip = prepare_monthly_averages(df, precip_var)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add temperature traces
    for year in df["year"].unique():
        year_temp = monthly_temp[monthly_temp["year"] == year]

        fig.add_trace(
            go.Scatter(
                x=year_temp["month_name"],
                y=year_temp[temp_var],
                name=f"Temperature {year}",
                mode="lines+markers",
                line=dict(width=2),
            ),
            secondary_y=False,
        )

    # Add precipitation traces
    for year in df["year"].unique():
        year_precip = monthly_precip[monthly_precip["year"] == year]

        fig.add_trace(
            go.Bar(
                x=year_precip["month_name"],
                y=year_precip[precip_var],
                name=f"Precipitation {year}",
                opacity=0.7,
            ),
            secondary_y=True,
        )

    # Set titles
    fig.update_layout(
        title_text="Temperature and Precipitation in the Sahel",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=50, b=0),
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Month")

    # Set y-axes titles
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
    fig.update_yaxes(title_text="Precipitation (mm)", secondary_y=True)

    return fig


def create_wind_rose_chart(df):
    """
    Create a wind rose chart showing wind speed distribution
    """
    # Group wind speed by month
    wind_by_month = df.groupby("month_name")["wind_speed_10m_max"].mean().reset_index()

    # Order months correctly
    wind_by_month["month_name"] = pd.Categorical(
        wind_by_month["month_name"],
        categories=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        ordered=True,
    )
    wind_by_month = wind_by_month.sort_values("month_name")

    # Create figure
    fig = px.bar_polar(
        wind_by_month,
        r="wind_speed_10m_max",
        theta="month_name",
        color="wind_speed_10m_max",
        title="Wind Speed Distribution by Month",
        color_continuous_scale="Viridis",
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, title="Wind Speed (km/h)")),
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig
