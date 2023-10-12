#import libaries 
# import pandas as pd
# import plotly.express as px
# import datetime as dt

#files
# file_2 = r'MyDashApp\ngsstats.xlsx'


# file_3 = r'MyDashApp\EIA_NG_Storage_Current.xlsx'


def pacific_storage(file2,file3):
    #import libaries 
    import pandas as pd
    import plotly.express as px
    import datetime as dt
    
    eia_storage_data = pd.read_excel(file2, sheet_name="ngsstats 2023 (2018-2022)", skiprows=2)
    eia_current_df = pd.read_excel(file3, skiprows=6)

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



    eia_current_df = eia_current_df.copy()
    eia_current_df.columns
    eia_current_df.rename(columns={'Week ending':'Date'}, inplace= True)
    eia_current_df = eia_current_df[["Date",'Mountain Region','Pacific Region']]



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


    eia_current_df.reset_index(drop=True, inplace=True)
    eia_storage_data.reset_index(drop=True, inplace=True)
    us_df = pd.concat([eia_storage_data, eia_current_df], axis=1)
    us_df.columns


    pacific_df = us_df[["date",'Pacific 5 Year Average','Pacific 5 Year Max','Pacific 5 Year Min','Pacific Working Gas Last Year','Pacific Region']]
    pacific_df


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
    # fig6.show()
    return fig6
