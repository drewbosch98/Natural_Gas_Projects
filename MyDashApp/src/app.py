# @ Create Time: 2023-10-10 11:14:02.627235

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
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

# #importing graphs from other files 
from moutain_storage import mountain_storage
from pacific_storage import pacific_storage
from ab_storage import alberta_storage
from bc_storage import british_columbia_storage
from western_storage import western_storage
from ng_pipeline_map import natural_gas_map

#intializations
app = Dash(__name__, title="MyDashApp", external_stylesheets=[dbc.themes.CYBORG])

#storage files
file1 = r'MyDashApp\filtered_storage_data.xlsx'
file2 = r'MyDashApp\ngsstats.xlsx'
file3 = r'MyDashApp\EIA_NG_Storage_Current.xlsx'

#geo map files 
hubs_file = r'MyDashApp\Natural_Gas_Trading_Hubs.xlsx'
eia_storage_file = r'MyDashApp\Natural_Gas_Underground_Storage.geojson'
eia_file = r'MyDashApp\Natural_Gas_Interstate_and_Intrastate_Pipelines.geojson'
file_4 = r'MyDashApp\NaturalGasUndergroundStorage_BC_AB.xlsx'

#Nautural Gas Pipleine, Storage, and Hub fMap 
fig1 = natural_gas_map(hubs_file,eia_storage_file,eia_file,file_4)

#Alberta Graph
fig2 = alberta_storage(file1)  
#British Columbia
fig3 = british_columbia_storage(file1)
#Western Canada
fig4 = western_storage(file1)
#Mountain US
fig5 = mountain_storage(file2,file3)
#Pacific US
fig6 = pacific_storage(file2,file3)



# layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H1("Natural Gas Fundamental Dashboard", style={'textAlign': 'center', 'color': 'blue'})], width=12)]),
    
    dbc.Row([
        dbc.Col([dcc.Graph(id="map", figure=fig1)], width=12),
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="selected_figure")], width=6),
        dbc.Col([
            dcc.Markdown('''
            # About This Project
            This is a current working project of mine that utilizes open-source data to create a centralized natural gas fundamental dashboard.
            It aims to identify key factors influencing price volatility in the Western North America natural gas market and potentially the WECC power market.
            This is an interactive dashboard that allows users to explore data using their mouse.
            
            Currently:
            Natural Gas Infrastrure Map 
            * United States: United States: Hubs, Storage, Interstate and Intrastate Pipelines
            * Canada: Hubs, Storage (Interstate and Intrastate Pipelines data is unavailable)
                
            Storage Tracker:
            * United States: Tracks both Pacific and Mountain storage levels (weekly)
            * Canada: Tracks Western Canada storage levels (monthly)

            Upcoming: 
            * Quatative demand forecast model to help predict future demand for various westcoast markets
            * Quatative storage model that that will predict storage level when their is excess supply in the market
            * Weather Tracker intergration to better understand key factors that are are drivng spot prices
            ''')], width=6)  
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                id="figure-selector",
                options=[
                    {'label': 'Western Canada Storage', 'value': 'fig4'},
                    {'label': 'Alberta Storage', 'value': 'fig2'},
                    {'label': 'BC Storage', 'value': 'fig3'},
                    {'label': 'Mountain Storage', 'value': 'fig5'},
                    {'label': 'Pacific Storage', 'value': 'fig6'},
                ],
                value='fig4',
                style={'fontColor': 'blue'},
                className="btn-group",
                labelClassName="btn btn-outline-primary",
            )], width=6)
    ])
], style={'width': '100%', 'height': '100vh', 'margin': 'auto'})


# Define the callback to update the selected figure
@app.callback(
    Output("selected_figure", "figure"),
    Input("figure-selector", "value")
)
def update_selected_figure(selected_value):
    # You should define fig2, fig3, and fig4 here or import them from elsewhere
    # For demonstration purposes, let's assume you have predefined these figures.
    if selected_value == 'fig2':
        return fig2
    elif selected_value == 'fig3':
        return fig3
    elif selected_value == 'fig4':
        return fig4
    elif selected_value == 'fig5':
        return fig5
    elif selected_value == 'fig6':
        return fig6
    
    else:
        # Return a default figure or an empty one if none of the options match
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
