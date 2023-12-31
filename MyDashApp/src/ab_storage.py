#Import libaries
import pandas as pd
from datetime import datetime 
import plotly.express as px

#file
file1 = r'MyDashApp\filtered_storage_data.xlsx'

def alberta_storage(file):
    #Alberta dataframes
    ab_open_df = pd.read_excel(file, sheet_name="AB_opening_inv")
    ab_close_df = pd.read_excel(file, sheet_name="AB_closing_inv")
    ab_inv_chg_df = pd.read_excel(file, sheet_name="AB_inv_chg")



    # Combining all the sheets together for 'ab'
    ab_df_names = [ab_open_df, ab_close_df, ab_inv_chg_df]
    ab_df = pd.concat(ab_df_names, ignore_index=True)

    # Renaming some columns
    ab_df.rename(columns={'REF_DATE': "Date", 'VALUE': 'm3'}, inplace=True)

    # Filtering out rows where "UOM" is "m3" and the "Date" is after January 1, 2021
    ab_df = ab_df[(ab_df["UOM"] == "Cubic metres") & (ab_df["Date"] >= datetime(2021, 1, 1))]
    
    # Converting m3 to BCF 
    ab_df['BCF'] = (ab_df["m3"]/28316846.6)*1000
    ab_df['Rolling_5_Year_Min_BCF'] = (ab_df["Rolling_5_Year_Min"] / 28316846.6) *1000
    ab_df['Rolling_5_Year_Max_BCF'] = (ab_df["Rolling_5_Year_max"] / 28316846.6)*1000
    ab_df['Avg_5_Year_BCF'] = (ab_df["Avg_5_Year"] / 28316846.6)*1000
    
    
    # Create custom legend names
    legend_names = {
        'BCF': 'Current Period',
        'Rolling_5_Year_Min_BCF': '5 Year Minimum',
        'Rolling_5_Year_Max_BCF': '5 Year Maximum',
        'Avg_5_Year_BCF': '5 Year Average'    
    }

    # Create the figure
    fig2 = px.line(ab_df, x='Date', y=['Rolling_5_Year_Min_BCF', 'Rolling_5_Year_Max_BCF','Avg_5_Year_BCF','BCF'], facet_row='Storage',
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
                                    '<b>Value (BCF)</b>: %{y}<br>')

    # Update trace names with custom legend names
    for trace in fig2.data:
        trace.name = legend_names.get(trace.name, '')

    # Update x-axis and y-axis titles
    # fig2.update_xaxes(title_text="Date")
    fig2.update_yaxes(title_text="BCF")

    # Move the legend to the bottom
    fig2.update_layout(legend=dict(x=0, y=-0.2, orientation="h"))

    # Change the color of the "5 Year Average" line to pink
    fig2.update_traces(selector=dict(name='5 Year Average'), line=dict(color='navy'))
    fig2.update_traces(selector=dict(name='5 Year Minimum'), line=dict(color='red'))
    fig2.update_traces(selector=dict(name='BCF'), line=dict(color='blue'))
    fig2.update_traces(selector=dict(name='5 Year Maximum'), line=dict(color='green'))

    #Showing the fig
    # fig2.show()
    return fig2
alberta_storage(file1)   
