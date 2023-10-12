# In[1]:

#imports
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import chart_studio.plotly as py
from datetime import datetime
import os
import geopandas as gpd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import date


app = Dash(__name__)


file = r'C:\Users\drewv\OneDrive - University of Calgary\Drew_HardDrive\Documents\Repositories\Natural_Gas_Projects\Canada Storagee Data\filtered_storage_data.xlsx'


# In[2]:


#Alberta dataframes
ab_open_df = pd.read_excel(file, sheet_name="AB_opening_inv")
ab_open_df
ab_close_df = pd.read_excel(file, sheet_name="AB_closing_inv")
ab_inv_chg_df = pd.read_excel(file, sheet_name="AB_inv_chg")

#BC dataframes
bc_open_df = pd.read_excel(file, sheet_name="BC_opening_inv")
bc_close_df = pd.read_excel(file, sheet_name="BC_closing_inv")
bc_inv_chg_df = pd.read_excel(file, sheet_name="BC_inv_chg")



# Combining all the sheets together for 'ab'
ab_df_names = [ab_open_df, ab_close_df, ab_inv_chg_df]
ab_df = pd.concat(ab_df_names, ignore_index=True)

# Renaming some columns
ab_df.rename(columns={'REF_DATE': "Date", 'VALUE': 'GJ'}, inplace=True)

# Filtering out rows where "UOM" is "Gigajoules" and the "Date" is after January 1, 2021
ab_df = ab_df[(ab_df["UOM"] == "Gigajoules") & (ab_df["Date"] >= datetime(2021, 1, 1))]

# Combining all the sheets together for 'bc'
bc_df_names = [bc_open_df, bc_close_df, bc_inv_chg_df]
bc_df = pd.concat(bc_df_names, ignore_index=True)

# Renaming some columns
bc_df.rename(columns={'REF_DATE': "Date", 'VALUE': 'GJ'}, inplace=True)

# Filtering out rows where "UOM" is "Gigajoules"
bc_df = bc_df[(bc_df["UOM"] == "Gigajoules") & (bc_df["Date"] >= datetime(2021, 1, 1))]






# Create custom legend names
legend_names = {
    'GJ': 'Current Period',
    'Rolling_5_Year_Min': '5 Year Minimum',
    'Rolling_5_Year_max': '5 Year Maximum',
    'Avg_5_Year': '5 Year Average'    
}

# Create the figure
fig2 = px.line(ab_df, x='Date', y=['GJ', 'Rolling_5_Year_Min', 'Rolling_5_Year_max','Avg_5_Year'], facet_row='Storage',
               title="Alberta Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0, facet_col_wrap=3)

# Update annotations to remove unwanted text
fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig2.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig2.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text=""  # Change the legend title to "Legend"
)

# Customize hovertemplate to show only the 'value'
fig2.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value (GJ)</b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig2.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
# fig2.update_xaxes(title_text="Date")
fig2.update_yaxes(title_text="GJ")

# Move the legend to the bottom
fig2.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the "5 Year Average" line to pink
fig2.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig2.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig2.update_traces(selector=dict(name='GJ'), line=dict(color='blue'))
fig2.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))




# Create custom legend names
legend_names = {
    'GJ': 'Current Period',
    'Rolling_5_Year_Min': '5 Year Minimum',
    'Rolling_5_Year_max': '5 Year Maximum',
    'Avg_5_Year': '5 Year Average'    
}

# Create the figure
fig3 = px.line(bc_df, x='Date', y=['GJ', 'Rolling_5_Year_Min', 'Rolling_5_Year_max','Avg_5_Year'], facet_row='Storage',
               title="British Columbia Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0, facet_col_wrap=3)

# Update annotations to remove unwanted text
fig3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig3.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig3.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text=""  # Change the legend title to "Legend"
)

# Customize hovertemplate to show only the 'value'
fig3.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value (GJ)</b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig3.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
# fig2.update_xaxes(title_text="Date")
fig3.update_yaxes(title_text="GJ")

# Move the legend to the bottom
fig3.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the "5 Year Average" line to pink
fig3.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig3.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig3.update_traces(selector=dict(name='GJ'), line=dict(color='blue'))
fig3.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))



ab_df.reset_index(drop=True, inplace=True)
bc_df.reset_index(drop=True, inplace=True)

# 'Rolling_5_Year_Min', 'Rolling_5_Year_max','Avg_5_Year']
GJ_df = ab_df["GJ"] + bc_df["GJ"]
Rolling_5_Year_Min_df = pd.DataFrame(ab_df["Rolling_5_Year_Min"] + bc_df["Rolling_5_Year_Min"])
Rolling_5_Year_max_df = pd.DataFrame(ab_df["Rolling_5_Year_max"] + bc_df["Rolling_5_Year_max"])
Avg_5_Year_df = pd.DataFrame(ab_df["Avg_5_Year"] + bc_df["Avg_5_Year"])

df_copy1 = ab_df.copy()
df_copy1 = df_copy1[['Date','Storage','UOM']]
df_copy1.reset_index(drop=True, inplace=True)


df_western = pd.concat([df_copy1,GJ_df,Rolling_5_Year_Min_df,Rolling_5_Year_max_df,Avg_5_Year_df], axis= 1)


# Create custom legend names
legend_names = {
    'GJ': 'Current Period',
    'Rolling_5_Year_Min': '5 Year Minimum',
    'Rolling_5_Year_max': '5 Year Maximum',
    'Avg_5_Year': '5 Year Average'    
}

# Create the figure
fig4 = px.line(df_western, x='Date', y=['GJ', 'Rolling_5_Year_Min', 'Rolling_5_Year_max','Avg_5_Year'], facet_row='Storage',
               title="Western Canada Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0, facet_col_wrap=3)

# Update annotations to remove unwanted text
fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig4.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig4.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text=""  # Change the legend title to "Legend"
)

# Customize hovertemplate to show only the 'value'
fig4.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value (GJ)</b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig4.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
# fig2.update_xaxes(title_text="Date")
fig4.update_yaxes(title_text="GJ")

# Move the legend to the bottom
fig4.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the "5 Year Average" line to pink

fig4.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig4.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig4.update_traces(selector=dict(name='GJ'), line=dict(color='blue'))
fig4.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))







# Retrieve the API token from the environment variable
api_token = os.environ.get("Mapbox_API_Token")

# Check if the API token is available
if api_token:
    print("API Token:", api_token)
else:
    print("API Token not found. Please check the variable name.")
hubs_df = pd.read_excel(r'C:\Users\drewv\OneDrive - University of Calgary\Drew_HardDrive\Documents\Repositories\Natural_Gas_Projects\Projects\Natural_Gas_Trading_Hubs.xlsx')
eia_storage_df = gpd.read_file(r'C:\Users\drewv\OneDrive - University of Calgary\Drew_HardDrive\Documents\Repositories\Natural_Gas_Projects\Projects\Natural_Gas_Underground_Storage.geojson')



eia_storage_df
import plotly.express as px
import geopandas as gpd
import shapely.geometry
import numpy as np
import wget




#filtering the eia df 
eia_storage_df = eia_storage_df[['Company','base_gas','work_cap','fld_cap','maxdeliv','Field_Type','Longitude','Latitude']]
eia_storage_df = eia_storage_df[(eia_storage_df['Longitude'] < -100)]


# Select the columns you want to format
columns_to_format = ['base_gas', 'work_cap', 'fld_cap', 'maxdeliv']

# Apply formatting to the selected columns
formatted_df = eia_storage_df.copy()  # Create a copy to avoid modifying the original DataFrame
formatted_df[columns_to_format] = formatted_df[columns_to_format].applymap('{:,.0f}'.format)

# Display the formatted DataFrame
formatted_df

# download a zipped shapefile
eia_df = gpd.read_file(r'C:\Users\drewv\OneDrive - University of Calgary\Drew_HardDrive\Documents\Repositories\Natural_Gas_Projects\Projects\Natural_Gas_Interstate_and_Intrastate_Pipelines.geojson')




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
filtered_df
#need to reload the data in 
df4 = pd.read_excel(r'Projects\NaturalGasUndergroundStorage_BC_AB.xlsx')
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
    hover_data=["Names"]
)

custom_hover_fig1 = "<b>Name:</b> %{customdata[0]}<br>" 
# Set the custom hover template for the scatter_mapbox trace in fig3
fig1.update_traces(
    hovertemplate=custom_hover_fig1,
)

# Create the scatter_mapbox trace
fig2 = px.scatter_mapbox(
    hubs_df,
    lat='Latitude',
    lon='Longitude',
    color='HubName',
    hover_name="HubName",
    hover_data=["HubName"]
)
custom_hover_fig2 = "<b>Hub:</b>" 
fig2.update_traces(
    marker={'size': 10},
    hovertemplate=custom_hover_fig2,
)

# USA Storage
fig3 = px.scatter_mapbox(
    formatted_df,
    lat='Latitude',
    lon='Longitude',
    color='Field_Type',
    hover_name='Company',
    hover_data=['Company', 'base_gas', 'work_cap', 'fld_cap', 'maxdeliv'],
    color_discrete_sequence=["navy", "red", "green"]
)

# Define a custom hover template 
custom_hover_template = "<b>Company:</b> %{customdata[0]}<br>" \
                        "<b>Base Gas:</b> %{customdata[1]}<br>" \
                        "<b>Working Gas Capacity:</b> %{customdata[2]}<br>" \
                        "<b>Field Capacity:</b> %{customdata[3]}<br>" \
                        "<b>Max Delivery:</b> %{customdata[4]}<br>"

# Set the custom hover template for the scatter_mapbox trace in fig3
fig3.update_traces(
    marker={'size': 7,},
    hovertemplate=custom_hover_template,
)

# Manually modify the legend to group "Depleted Field" together
fig3.update_traces(
    showlegend=True,  
    selector=dict(name='Depleted Field'),  
    legendgroup='Depleted Field', 
)

# Canada Storage
fig4 = px.scatter_mapbox(
    df4_copy,
    lat='Latitude',
    lon='Longitude',
    color='Field Type',
    hover_name='Company',
    hover_data=['Field Type', 'Working Gas Capacity (MMcf)'],
    color_discrete_sequence=["navy", "red", "green"]
)

# Define a custom hover template using %{...} placeholders for fig4
custom_hover_template_fig4 = "<b>Company:</b> %{hovertext}<br>" \
                             "<b>Working Gas Capacity (MMcf):</b> %{customdata[1]}<br>"

# Set the custom hover template for the scatter_mapbox trace in fig4
fig4.update_traces(
    marker={'size': 7,},
    hovertemplate=custom_hover_template_fig4,
)

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
    mapbox_zoom=4,
    paper_bgcolor='black',  # Set the background color of the entire plot
    plot_bgcolor='black'   # Set the background color of the plot area
)


# Set the background color for the legend
fig1.update_layout(legend=dict(
        bgcolor='black',
        title_font_color='white',  # Change the title font color to white
        title_font_size=12  # Adjust the title font size as needed
    ))





# Define your Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Define your layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H1("Natural Gas Fundamental Dashboard", style={'textAlign': 'center'})], width=12)]),
    
    dbc.Row([
        dbc.Col([dcc.Graph(id="map", figure=fig1)], width=12),
        dbc.Col([
            dcc.RadioItems(
                id="figure-selector",
                options=[
                    {'label': 'Western Canada Storage', 'value': 'fig4'},
                    {'label': 'Alberta Storage', 'value': 'fig2'},
                    {'label': 'BC Storage', 'value': 'fig3'}
                    
                ],
                value='fig4'  # Default value when the app starts
            ),
            dcc.Graph(id="selected_figure")
        ], width=6)
    ]),
], 
                           style={'backgroundColor': 'black'})  # Set the background color to black

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
    else:
        # Return a default figure or an empty one if none of the options match
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)



file_2 = r'C:\Users\drewv\OneDrive - University of Calgary\Drew_HardDrive\Documents\Repositories\Natural_Gas_Projects\EIA S&D Data\ngsstats.xlsx'
eia_storage_data = pd.read_excel(file_2, sheet_name="ngsstats 2023 (2018-2022)", skiprows=2)
eia_storage_data.columns

eia_storage_df = eia_storage_data.copy()

eia_storage_data.rename(columns={'Report Date':'date',
                                 'Mountain':'Mountain 5 Year Average',
                                 'Pacific': 'Pacific 5 Year Average',
                                 'Mountain.1':'Mountain 5 Year Max',
                                 'Pacific.1':'Pacific 5 Year Max',
                                 'Mountain.2': 'Mountain 5 Year Min',
                                 'Pacific.2': 'Pacific 5 Year Min',
                                 'Mountain.3': 'Mountain Working Gas Last Year',
                                 'Pacific.3': 'Pacific Working Gas Last Year'}, inplace= True)
eia_storage_data = eia_storage_data[['date','Mountain 5 Year Average','Pacific 5 Year Average',
                  'Mountain 5 Year Max','Pacific 5 Year Max',
                  'Mountain 5 Year Min','Pacific 5 Year Min',
                  'Mountain Working Gas Last Year','Pacific Working Gas Last Year']]



eia_storage_data.tail()




file_3 = r'C:\Users\drewv\OneDrive - University of Calgary\Drew_HardDrive\Documents\Repositories\Natural_Gas_Projects\EIA S&D Data\EIA_NG_Storage_Current.xlsx'
eia_current_df = pd.read_excel(file_3, skiprows=6)
eia_current_df = eia_current_df.copy()
eia_current_df.columns
eia_current_df.rename(columns={'Week ending':'Date'}, inplace= True)
eia_current_df = eia_current_df[["Date",'Mountain Region','Pacific Region']]



eia_current_df.head()


# In[ ]:


import pandas as pd


# Assuming your DataFrame is named eia_current_df

# Convert 'Date' column to datetime format
eia_current_df['Date'] = pd.to_datetime(eia_current_df['Date'], errors='coerce')

# Filter the DataFrame for dates greater than or equal to '2023-01-06'
eia_current_df = eia_current_df[eia_current_df["Date"] >= dt.datetime(2023, 1, 6)]

# Format the 'Date' column to 'year-month-day'
eia_current_df['Date'] = eia_current_df['Date'].dt.strftime('%Y-%m-%d')

# Now, assuming you have another DataFrame named eia_storage_data

# Convert 'Date' column in eia_storage_data to datetime format
eia_storage_data['date'] = pd.to_datetime(eia_storage_data['date'], errors='coerce')

# Filter eia_storage_data based on the same date condition
eia_storage_data = eia_storage_data[(eia_storage_data["date"] >= dt.datetime(2023, 1, 6)) & (eia_storage_data["date"] <= dt.datetime(2023, 12, 1)) ]

# Display the updated DataFrames
eia_storage_data


# In[ ]:




# In[ ]:



# In[ ]:


eia_current_df.reset_index(drop=True, inplace=True)
eia_storage_data.reset_index(drop=True, inplace=True)
us_df = pd.concat([eia_storage_data, eia_current_df], axis=1)
us_df.columns


# In[ ]:


mountain_df = us_df[['date','Mountain 5 Year Average','Mountain 5 Year Max','Mountain 5 Year Min','Mountain Working Gas Last Year','Mountain Region']]
mountain_df

pacific_df = us_df[["date",'Pacific 5 Year Average','Pacific 5 Year Max','Pacific 5 Year Min','Pacific Working Gas Last Year','Pacific Region']]
pacific_df




import plotly.express as px
import plotly.graph_objects as go

# Create custom legend names
legend_names = {
    'Mountain 5 Year Average': '5 Year Average',
    'Mountain 5 Year Max': '5 Year Maximum',
    'Mountain 5 Year Min': '5 Year Minimum',
    'Mountain Region': 'Current Period'
}

# Create the figure
fig5 = px.line(mountain_df, x='date', y=['Mountain 5 Year Average', 'Mountain 5 Year Max', 'Mountain 5 Year Min', 'Mountain Region'],
               title="Mountain Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0)

# Update annotations to remove unwanted text
fig5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig5.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig5.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text="Legend"
)

# Customize hovertemplate to show only the 'value'
fig5.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value </b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig5.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
fig5.update_xaxes(title_text="Date")
fig5.update_yaxes(title_text="BCF")

# Move the legend to the bottom
fig5.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the lines
fig5.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig5.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig5.update_traces(selector=dict(name='Current Period'), line=dict(color='blue'))
fig5.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))

# # Show the plot
fig5.show()


# In[ ]:


import plotly.express as px
import plotly.graph_objects as go

# Create custom legend names
legend_names = {
    'Pacific 5 Year Average': '5 Year Average',
    'Pacific 5 Year Max': '5 Year Maximum',
    'Pacific 5 Year Min': '5 Year Minimum',
    'Pacific Region': 'Current Period'
}

# Create the figure
fig6 = px.line(pacific_df, x='date', y=['Pacific 5 Year Average', 'Pacific 5 Year Max', 'Pacific 5 Year Min', 'Pacific Region'],
               title="Pacific Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0)

# Update annotations to remove unwanted text
fig6.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig6.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig6.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text="Legend"
)

# Customize hovertemplate to show only the 'value'
fig6.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value </b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig6.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
fig6.update_xaxes(title_text="Date")
fig6.update_yaxes(title_text="BCF")

# Move the legend to the bottom
fig6.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the lines
fig6.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig6.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig6.update_traces(selector=dict(name='Current Period'), line=dict(color='blue'))
fig6.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))

# # Show the plot
fig6.show()


# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import date


# # Define your Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# # Define your layout
# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([html.H1("Natural Gas Fundamental Dashboard", style={'textAlign': 'center'})], width=12)]),
    
#     dbc.Row([
#         dbc.Col([dcc.Graph(id="map", figure=fig1)], width=12),
#         dbc.Col([
#             dcc.RadioItems(
#                 id="figure-selector",
#                 options=[
#                     {'label': 'Western Canada Storage', 'value': 'fig4'},
#                     {'label': 'Alberta Storage', 'value': 'fig2'},
#                     {'label': 'BC Storage', 'value': 'fig3'},
#                     {'label': 'Pacific Storage', 'value': 'fig5'},
#                     {'label': 'Mountain Storage', 'value': 'fig6'},
                    
                    
#                 ],
#                 value='fig4'  # Default value when the app starts
#             ),
#             dcc.Graph(id="selected_figure")
#         ], width=6)
#     ],
#             ),
# ], 
#                            style={'backgroundColor': 'black'})  # Set the background color to black

# # Define the callback to update the selected figure
# @app.callback(
#     Output("selected_figure", "figure"),
#     Input("figure-selector", "value")
# )
# def update_selected_figure(selected_value):
#     # You should define fig2, fig3, and fig4 here or import them from elsewhere
#     # For demonstration purposes, let's assume you have predefined these figures.
#     if selected_value == 'fig2':
#         return fig2
#     elif selected_value == 'fig3':
#         return fig3
#     elif selected_value == 'fig4':
#         return fig4
#     elif selected_value == 'fig5':
#         return fig5
#     elif selected_value == 'fig6':
#         return fig6
    
#     else:
#         # Return a default figure or an empty one if none of the options match
#         return {}

# if __name__ == '__main__':
#     app.run_server(debug=True)


# In[ ]:


import plotly.express as px
import plotly.graph_objects as go

# Create custom legend names
legend_names = {
    'GJ': 'Current Period',
    'Rolling_5_Year_Min': '5 Year Minimum',
    'Rolling_5_Year_max': '5 Year Maximum',
    'Avg_5_Year': '5 Year Average'    
}

# Create the figure
fig2 = px.line(ab_df, x='Date', y=['GJ', 'Rolling_5_Year_Min', 'Rolling_5_Year_max','Avg_5_Year'], facet_row='Storage',
               title="Alberta Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0, facet_col_wrap=3)

# Update annotations to remove unwanted text
fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig2.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig2.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text=""  # Change the legend title to "Legend"
)

# Customize hovertemplate to show only the 'value'
fig2.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value (GJ)</b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig2.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
# fig2.update_xaxes(title_text="Date")
fig2.update_yaxes(title_text="GJ")

# Move the legend to the bottom
fig2.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the "5 Year Average" line to pink

fig2.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig2.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig2.update_traces(selector=dict(name='GJ'), line=dict(color='blue'))
fig2.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))


# Show the plot
fig2.show()


# In[ ]:


import plotly.express as px
import plotly.graph_objects as go

# Create custom legend names
legend_names = {
    'GJ': 'Current Period',
    'Rolling_5_Year_Min': '5 Year Minimum',
    'Rolling_5_Year_max': '5 Year Maximum',
    'Avg_5_Year': '5 Year Average'    
}

# Create the figure
fig3 = px.line(bc_df, x='Date', y=['GJ', 'Rolling_5_Year_Min', 'Rolling_5_Year_max','Avg_5_Year'], facet_row='Storage',
               title="British Columbia Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0, facet_col_wrap=3)

# Update annotations to remove unwanted text
fig3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig3.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig3.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text=""  # Change the legend title to "Legend"
)

# Customize hovertemplate to show only the 'value'
fig3.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value (GJ)</b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig3.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
# fig2.update_xaxes(title_text="Date")
fig3.update_yaxes(title_text="GJ")

# Move the legend to the bottom
fig3.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the "5 Year Average" line to pink

fig3.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig3.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig3.update_traces(selector=dict(name='GJ'), line=dict(color='blue'))
fig3.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))


# Show the plot
fig3.show()


# In[ ]:


import plotly.express as px
import plotly.graph_objects as go

# Create custom legend names
legend_names = {
    'GJ': 'Current Period',
    'Rolling_5_Year_Min': '5 Year Minimum',
    'Rolling_5_Year_max': '5 Year Maximum',
    'Avg_5_Year': '5 Year Average'    
}

# Create the figure
fig4 = px.line(df_western, x='Date', y=['GJ', 'Rolling_5_Year_Min', 'Rolling_5_Year_max','Avg_5_Year'], facet_row='Storage',
               title="Western Canada Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0, facet_col_wrap=3)

# Update annotations to remove unwanted text
fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig4.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig4.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text=""  # Change the legend title to "Legend"
)

# Customize hovertemplate to show only the 'value'
fig4.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value (GJ)</b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig4.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
# fig2.update_xaxes(title_text="Date")
fig4.update_yaxes(title_text="GJ")

# Move the legend to the bottom
fig4.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the "5 Year Average" line to pink

fig4.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig4.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig4.update_traces(selector=dict(name='GJ'), line=dict(color='blue'))
fig4.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))


# Show the plot
fig4.show()


# In[ ]:


import plotly.express as px
import plotly.graph_objects as go

# Create custom legend names
legend_names = {
    'Mountain 5 Year Average': '5 Year Average',
    'Mountain 5 Year Max': '5 Year Maximum',
    'Mountain 5 Year Min': '5 Year Minimum',
    'Mountain Region': 'Current Period'
}

# Create the figure
fig5 = px.line(mountain_df, x='date', y=['Mountain 5 Year Average', 'Mountain 5 Year Max', 'Mountain 5 Year Min', 'Mountain Region'],
               title="Mountain Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0)

# Update annotations to remove unwanted text
fig5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig5.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig5.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text="Legend"
)

# Customize hovertemplate to show only the 'value'
fig5.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value (BCF)</b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig5.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
fig5.update_xaxes(title_text="Date")
fig5.update_yaxes(title_text="BCF")

# Move the legend to the bottom
fig5.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the lines
fig5.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig5.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig5.update_traces(selector=dict(name='Current Period'), line=dict(color='blue'))
fig5.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))

# # Show the plot
fig5.show()


# In[ ]:


import plotly.express as px
import plotly.graph_objects as go

# Create custom legend names
legend_names = {
    'Pacific 5 Year Average': '5 Year Average',
    'Pacific 5 Year Max': '5 Year Maximum',
    'Pacific 5 Year Min': '5 Year Minimum',
    'Pacific Region': 'Current Period'
}

# Create the figure
fig6 = px.line(pacific_df, x='date', y=['Pacific 5 Year Average', 'Pacific 5 Year Max', 'Pacific 5 Year Min', 'Pacific Region'],
               title="Pacific Natural Gas Storage",
               facet_row_spacing=0.0, facet_col_spacing=0.0)

# Update annotations to remove unwanted text
fig6.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Update y-axes to not have any shared scales
fig6.update_yaxes(matches=None)

# Update the layout with the dark template and center-aligned title
fig6.update_layout(
    template="plotly_dark",
    title_x=0.5,
    height=600,
    width=600,
    legend_title_text="Legend"
)

# Customize hovertemplate to show only the 'value'
fig6.update_traces(hovertemplate='<b>Date</b>: %{x}<br>'
                                '<b>Value (BCF)</b>: %{y}<br>')

# Update trace names with custom legend names
for trace in fig6.data:
    trace.name = legend_names.get(trace.name, '')

# Update x-axis and y-axis titles
fig6.update_xaxes(title_text="Date")
fig6.update_yaxes(title_text="BCF")

# Move the legend to the bottom
fig6.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

# Change the color of the lines
fig6.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
fig6.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
fig6.update_traces(selector=dict(name='Current Period'), line=dict(color='blue'))
fig6.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))

# # Show the plot
fig6.show()


# In[ ]:


# Define your Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Define your layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H1("Natural Gas Fundamental Dashboard", style={'textAlign': 'center'})], width=12)]),
    
    dbc.Row([
        dbc.Col([dcc.Graph(id="map", figure=fig1)], width=12),
        dbc.Col([
            dcc.RadioItems(
                id="figure-selector",
                options=[
                    {'label': 'Western Canada Storage', 'value': 'fig4'},
                    {'label': 'Alberta Storage', 'value': 'fig2'},
                    {'label': 'BC Storage', 'value': 'fig3'},
                    {'label': 'Pacific Storage', 'value': 'fig5'},
                    {'label': 'Mountain Storage', 'value': 'fig6'},
                    
                    
                ],
                value='fig4'  # Default value when the app starts
            ),
            dcc.Graph(id="selected_figure")
        ], width=6)
    ],
            ),
], 
                           style={'backgroundColor': 'black'})  # Set the background color to black

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






