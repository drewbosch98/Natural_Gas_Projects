#imports
import pandas as pd
import datetime as dt
import plotly.express as px
import numpy as np
from datetime import datetime
import os
import geopandas as gpd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Define your Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], title="MyApp")  # Define the app here
server = app.server





#importing graphs from other files 
from MyDashApp.src.moutain_storage import mountain_storage
from MyDashApp.src.pacific_storage import pacific_storage
from MyDashApp.src.ab_storage import alberta_storage
from MyDashApp.src.bc_storage import british_columbia_storage
from MyDashApp.src.western_storage import western_storage
from MyDashApp.src.ng_pipeline_map import natural_gas_map


# Define your layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H1("Natural Gas Fundamental Dashboard", style={'textAlign': 'center'})], width=12)]),
    
    dbc.Row([
        dbc.Col([dcc.Graph(id="map", figure=natural_gas_map)], width=12),
        dbc.Col([
            dcc.RadioItems(
                id="figure-selector",
                options=[
                    {'label': 'Western Canada Storage', 'value': 'western_storage'},
                    {'label': 'Alberta Storage', 'value': 'alberta_storage'},
                    {'label': 'BC Storage', 'value': 'british_columbia_storage'},
                    {'label': 'Pacific Storage', 'value': 'pacific_storage'},
                    {'label': 'Mountain Storage', 'value': 'mountain_storage'},
                ],
                value='western_storage'  # Default value when the app starts
            ),
            dcc.Graph(id="selected_figure")
        ], width=6)
    ]),
], style={'backgroundColor': 'black'})  # Set the background color to black

# Define the callback to update the selected figure
@app.callback(
    Output("selected_figure", "figure"),
    Input("figure-selector", "value")
)
def update_selected_figure(selected_value):
    # You should define fig2, fig3, and fig4 here or import them from elsewhere
    # For demonstration purposes, let's assume you have predefined these figures.
    if selected_value == 'alberta_storage':
        return alberta_storage
    elif selected_value == 'british_columbia_storage':
        return british_columbia_storage
    elif selected_value == 'western_storage':
        return western_storage
    elif selected_value == 'mountain_storage':
        return mountain_storage
    elif selected_value == 'pacific_storage':
        return pacific_storage
    else:
        # Return a default figure or an empty one if none of the options match
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
