# First Natural Gas Dashboard using Plotly and Dash
import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from dash.dependencies import Input, Output

# Initialize the app
app = Dash(__name__)

# Sample data, replace with your CSV file path
data = pd.read_csv("ngtl-throughput-and-capacity.csv")
df = pd.DataFrame(data)

# Parsing the dataframe to only include certain columns of data
df = df[['Date', 'Day', 'Month', 'Year', 'Key Point', 'Latitude', 'Longitude', 'Direction Of Flow', 'Capacity (1000 m3/d)', 'Throughput (1000 m3/d)', 'Throughput (GJ/d)']]

# Filtering the data
df = df[df["Date"] >= "2022-01-01"]
df = df.groupby(by=["Key Point", "Year", "Month", "Latitude", "Longitude", "Direction Of Flow"]).sum()
df = df.reset_index()
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%m')

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is'''


# App layout this where the layout of the dashboard is created
app.layout = html.Div([
    
    html.H1(children = 'NGTL Dashboard', style = {'textAlign': 'center',}),
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.RadioItems(options=[{'label': 'Capacity (1000 m3/d)', 'value': 'Capacity (1000 m3/d)'},
            {'label': 'Throughput (1000 m3/d)', 'value': 'Throughput (1000 m3/d)'},
            {'label': 'Throughput (GJ/d)', 'value': 'Throughput (GJ/d)'}],
        value='Throughput (GJ/d)',
        id='controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(id='controls-and-graph',figure={},),
    dcc.Markdown(children=markdown_text)
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    filtered_df = df[['Date', 'Key Point', col_chosen]]
    fig = px.bar(
        filtered_df, x="Date", y=col_chosen, color="Key Point",
        title=f"Natural Gas Flows NGTL - {col_chosen}",
        labels={'Date': 'Date (Months)', col_chosen: f'{col_chosen} (GJ/day)'}
    )
    fig.update_layout(xaxis_tickangle=45, xaxis=dict(tickvals=filtered_df["Date"]))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
