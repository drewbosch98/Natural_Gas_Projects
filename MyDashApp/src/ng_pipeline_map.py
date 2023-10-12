def natural_gas_map(hubs_file,eia_storage_file,eia_file,file_4):
    import pandas as pd 
    import numpy as np 
    import seaborn as sns
    import chart_studio.plotly as py
    import plotly.express as px
    from datetime import datetime
    import os
    import geopandas as gpd
    from dash import Dash, html, dcc
    import dash_bootstrap_components as dbc
    from dash_bootstrap_templates import load_figure_template
    app = Dash(__name__)
        
    
    
    hubs_df = pd.read_excel(hubs_file)
    eia_storage_df = gpd.read_file(eia_storage_file)
    eia_df = gpd.read_file(eia_file)
    df4 = pd.read_excel(file_4)
    
    # Retrieve the API token from the environment variable
    api_token = os.environ.get("Mapbox_API_Token")

    # Check if the API token is available
    if api_token:
        print("API Token found")
    else:
        print("API Token not found. Please check the variable name.")



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

    # Show the combined figure
    # fig1.show()
    return fig1
