#Import libaries
import pandas as pd
from datetime import datetime 
import plotly.express as px

#file
file = r'MyDashApp\filtered_storage_data.xlsx'

def western_storage(file):
    
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
    df_western

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
    # fig4.show()
    return fig4
    
western_storage(file)