#imports
import pandas as pd 
import numpy as np 
import seaborn as sns
import chart_studio.plotly as py
import plotly.express as px
from datetime import datetime
import os
import geopandas as gpd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import Dash, html, dcc
import shapely.geometry
import wget
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


# Retrieve the API token from the environment variable
api_token = os.environ.get("Mapbox_API_Token")

# Check if the API token is available
if api_token:
    print("API Token:", api_token)
else:
    print("API Token not found. Please check the variable name.")
    
    
#files 
hubs_df = pd.read_excel(r'Natural_Gas_Trading_Hubs.xlsx')
eia_storage_df = gpd.read_file(r'ShapeFiles/Natural_Gas_Underground_Storage.geojson')
eia_storage_df = gpd.read_file(r'ShapeFiles/Natural_Gas_Underground_Storage.geojson')

#filtering the eia df 
eia_storage_df = eia_storage_df[['Company','base_gas','work_cap','fld_cap','maxdeliv','Field_Type','Longitude','Latitude']]
eia_storage_df = eia_storage_df[(eia_storage_df['Longitude'] < -100)]


# Select the columns you want to format
columns_to_format = ['base_gas', 'work_cap', 'fld_cap', 'maxdeliv']

# Apply formatting to the selected columns
formatted_df = eia_storage_df.copy()  # Create a copy to avoid modifying the original DataFrame
formatted_df[columns_to_format] = formatted_df[columns_to_format].applymap('{:,.0f}'.format)

# download a zipped shapefile
eia_df = gpd.read_file(r'C:\Users\drewv\OneDrive - University of Calgary\Drew_HardDrive\Documents\Repositories\Natural_Gas_Projects\ShapeFiles\Natural_Gas_Interstate_and_Intrastate_Pipelines.geojson')




lats = []
lons = []
names = []

for feature, name in zip(eia_df.geometry, eia_df.Operator):
    if isinstance(feature, shapely.geometry.linestring.LineString):
        linestrings = [feature]
    elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
        linestrings = feature.geoms
    else:
        continue
    for linestring in linestrings:
        x, y = linestring.xy
        lats = np.append(lats, y)
        lons = np.append(lons, x)
        names = np.append(names, [name]*len(y))
        lats = np.append(lats, None)
        lons = np.append(lons, None)
        names = np.append(names, None)

eia_filter_df = pd.DataFrame({'Names':names,'lats':lats, 'lons':lons})
filtered_df = eia_filter_df[(eia_filter_df['lons'] < -100.00 ) | (eia_filter_df['lons'].isna())]

df4 = pd.read_excel(r'C:\Users\drewv\OneDrive - University of Calgary\Drew_HardDrive\Documents\Repositories\Natural_Gas_Projects\ShapeFiles\NaturalGasUndergroundStorage_BC_AB.xlsx')
df4
df4_copy = df4.copy()
df4_copy['Working Gas Capacity (MMcf)'] = df4_copy['Working Gas Capacity (MMcf)'].apply('{:,.0f}'.format)
df4_copy.rename(columns={'Owner Name (Company)':'Company'}, inplace=True)
df4_copy


import plotly.express as px

# Create the line_mapbox figure
fig1 = px.line_mapbox(
    filtered_df,
    lat="lats",  # Replace with the actual column name for latitude
    lon="lons",  # Replace with the actual column name for longitude
    hover_name="Names",  # Replace with the actual column name for hover labels
    mapbox_style="stamen-terrain",
    zoom=1,
    template="CYBORG"
)

# Create the scatter_mapbox trace
fig2 = px.scatter_mapbox(
    hubs_df,
    lat='Latitude',
    lon='Longitude',
    color='HubName'
)
fig2.update_traces(marker={'size': 10})


#USA Storage
fig3 = px.scatter_mapbox(
    eia_storage_df,
    lat='Latitude',
    lon='Longitude',
    color='Field_Type',
    hover_name= 'Company',
    hover_data= ['Company','Field_Type','base_gas','work_cap','fld_cap','maxdeliv'],

)
fig3.update_traces(marker={'size': 7})
fig3.update_traces(
    hovertemplate="<b>Company:</b> %{hovertext}<br>"
                  "<b>Type:</b> %{customdata[0]}<br>"
                  "<b>Total Field Capacity:</b> %{customdata[1]}<br>"
                  "<b>Base Gas:</b> %{customdata[2]}<br>"
                  "<b>Working Gas Capacity:</b> %{customdata[3]}<br>"
                  "<b>Max Daily Delivery:</b> %{customdata[4]}<extra></extra>",
    customdata=formatted_df[['Field_Type', 'fld_cap', 'base_gas', 'work_cap', 'maxdeliv']].values
)

#Canada Storage
fig4 = px.scatter_mapbox(
    df4_copy,
    lat='Latitude',
    lon='Longitude',
    color='Field Type',
    hover_name='Company',  # Replace with the actual column name for the company name
    hover_data=['Field Type', 'Working Gas Capacity (MMcf)'],  # Make sure column names are correct
)
fig4.update_traces(marker={'size': 7})
# fig4.update_traces(
#     hovertemplate="<b>Company:</b> %{hovertext}<br>"
#                   "<b>Type:</b> %{customdata[0]}<br>"
#                   "<b>Working Gas Capacity:</b> %{customdata[1]}<br>",
#     customdata=df4_copy[['Field Type', 'Working Gas Capacity (MMcf)']].values
# )



# Add the scatter_mapbox trace to the line_mapbox figure
for trace in fig2.data:
    fig1.add_trace(trace)

for trace in fig3.data:
    fig1.add_trace(trace)
    
for trace in fig4.data:
    fig1.add_trace(trace)
    

# Update the layout of the combined figure
fig1.update_layout(
    mapbox_style="dark",
    mapbox_accesstoken=api_token,  # Replace with your Mapbox API token
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox_center={"lat": 51.5461, "lon": -113.4937},
    mapbox_zoom=4
)

# Show the combined figure
fig1.show()


