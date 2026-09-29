#!/usr/bin/env python
# coding: utf-8

# Final Assignment: Part 2 - Create Dashboard with Plotly and Dash
# Automobile Sales Statistics Dashboard

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the IBM course dataset
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "historical_automobile_sales.csv"
)
data = pd.read_csv(DATA_URL)

# Initialize Dash application
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]
year_list = [i for i in range(1980, 2024, 1)]

# TASK 2.1 + 2.2 + 2.3
app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={"textAlign": "center", "color": "#503D36", "font-size": 24},
    ),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id="dropdown-statistics",
            options=dropdown_options,
            value="Yearly Statistics",
            placeholder="Select a report type",
            style={"width": "80%", "padding": "3px", "font-size": 20},
        ),
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="select-year",
            options=[{"label": i, "value": i} for i in year_list],
            value=1980,
            placeholder="Select a year",
            style={"width": "80%", "padding": "3px", "font-size": 20},
        ),
    ]),

    html.Div(id="output-container", className="chart-grid",
             style={"display": "flex", "flexWrap": "wrap"})
])

# TASK 2.4 - Enable year dropdown only for Yearly Statistics
@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_statistics):
    return selected_statistics != "Yearly Statistics"


# TASK 2.5 - Create and display graphs
@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="dropdown-statistics", component_property="value"),
        Input(component_id="select-year", component_property="value"),
    ],
)
def update_output_container(selected_statistics, input_year):

    if selected_statistics == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        # Plot 1: Average automobile sales during recession
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales during Recession",
            )
        )

        # Plot 2: Average vehicles sold by vehicle type
        avg_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Vehicles Sold by Vehicle Type during Recession",
            )
        )

        # Plot 3: Advertising expenditure share by vehicle type
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Advertising Expenditure Share by Vehicle Type during Recession",
            )
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales
        R_chart4 = dcc.Graph(
            figure=px.bar(
                recession_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
                barmode="group",
            )
        )

        return [
            html.Div(R_chart1, style={"width": "50%"}),
            html.Div(R_chart2, style={"width": "50%"}),
            html.Div(R_chart3, style={"width": "50%"}),
            html.Div(R_chart4, style={"width": "50%"}),
        ]

    elif selected_statistics == "Yearly Statistics" and input_year is not None:
        yearly_data = data[data["Year"] == input_year]

        # Plot 1: Yearly average automobile sales over all years
        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Yearly Average Automobile Sales",
            )
        )

        # Plot 2: Total monthly automobile sales for selected year
        monthly_sales = (
            yearly_data.groupby("Month")["Automobile_Sales"]
            .sum()
            .reset_index()
        )
        Y_chart2 = dcc.Graph(
            figure=px.line(
                monthly_sales,
                x="Month",
                y="Automobile_Sales",
                title=f"Total Monthly Automobile Sales in {input_year}",
            )
        )

        # Plot 3: Average sales by vehicle type for selected year
        avg_vehicle = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avg_vehicle,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=f"Average Automobile Sales by Vehicle Type in {input_year}",
            )
        )

        # Plot 4: Total advertisement expenditure by vehicle type
        ad_exp = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                ad_exp,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=f"Advertisement Expenditure by Vehicle Type in {input_year}",
            )
        )

        return [
            html.Div(Y_chart1, style={"width": "50%"}),
            html.Div(Y_chart2, style={"width": "50%"}),
            html.Div(Y_chart3, style={"width": "50%"}),
            html.Div(Y_chart4, style={"width": "50%"}),
        ]

    return html.Div("Please select a report type and year.")


if __name__ == "__main__":
    app.run(debug=True)
