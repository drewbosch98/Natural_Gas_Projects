# First Natural Gas Dashboard using Plotly and Dash
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
from dash.dependencies import Input, Output

# Initialize the app
app = Dash(__name__)

# Sample data, replace with your CSV file path
data = pd.read_csv("ngtl-throughput-and-capacity.csv")
df = pd.DataFrame(data)

# Parsing the dataframe to only include certain columns of data
df = df[['Date', 'Day', 'Month', 'Year', 'Key Point', 'Latitude', 'Longitude', 'Direction Of Flow', 'Capacity (1000 m3/d)', 'Throughput (1000 m3/d)', 'Throughput (GJ/d)']]

# Filtering the data
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
    html.H1(children='NGTL Dashboard', style={'textAlign': 'center'}),
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.DatePickerRange(
        start_date=min(df['Date']),
        end_date=max(df['Date']),
        display_format='YYYY-MM',
        id='date-range-picker'
    ),
    dcc.Graph(id='graph-with-slider', figure={}),
    dcc.Markdown(children=markdown_text)
])

# Add controls to build the interaction
@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_figure(start_date, end_date):
    filtered_df = df[(df.Date >= start_date) & (df.Date <= end_date)]
    fig = px.bar(filtered_df, x="Date", y='Throughput (GJ/d)',
                 color="Key Point", labels={'Date': 'Date (Months)'})
    fig.update_layout(transition_duration=500)
    fig.update_layout(xaxis_tickangle=45, xaxis=dict(tickvals=filtered_df["Date"]))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
