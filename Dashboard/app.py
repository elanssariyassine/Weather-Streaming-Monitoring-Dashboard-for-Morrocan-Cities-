import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import datetime as dt
import time
import pandas as pd

# Dash Application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True

# Initialize the current refresh time and temperature variables
current_refresh_time_temp = None

# For Data Table
api_endpoint = "http://localhost:8090/wm/v1"  # Fix the typo "localhist" to "localhost"
api_response = requests.get(api_endpoint)
record_list = api_response.json()
df = pd.DataFrame(record_list, columns=["CityName", "Temperature", "Humidity", "CreationTime", "CreationDate"])
df["index"] = range(1, len(df) + 1)

PAGE_SIZE = 5

# Assign HTML content to Dash app layout
app.layout = html.Div(
    [
        html.H2(
            children="Real Time Weather Monitoring Dashboard",
            style={
                "textAlign": "center",
                "color": "#720443",
                "font-weight": "bold",
                "font-family": "Verdana"
            }),
        html.Br(),
        html.Div(
            id="current_time",
            children="Current time",
            style={
                "textAlign": "center",
                "color": "black",
                "font-weight": "bold",
                "fontSize": 10,
                "font-family": "Verdana"
            }
        ),
        html.Div([
            dcc.Graph(id='live-update-graph-bar')
        ], className="six columns"),
        html.Div([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dash_table.DataTable(
                id='datatable-paging',
                columns=[{"name": i, "id": i} for i in sorted(["CityName", "Temperature", "Humidity",
                                                               "CreationTime", "CreationDate"])],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action="custom"
            )
        ], className="six columns"),
    ], className="row"
)

app.layout.children.append(
    dcc.Interval(
        id="interval-component",
        interval=1000,
        n_intervals=0
    )
)


@app.callback(
    Output("current_time", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_layout(n):
    global current_refresh_time_temp
    current_refresh_time_temp = time.strftime("%Y-%m-%d %H:%M:%S")
    return "Current Refresh Time: {}".format(current_refresh_time_temp)


@app.callback(
    Output("live-update-graph-bar", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_graph_bar(n):
    traces = []
    bar_1 = go.Bar(
        x=df["CityName"].head(5),
        y=df["Temperature"].head(5),
        name="Temperature"
    )
    traces.append(bar_1)

    bar_2 = go.Bar(
        x=df["CityName"].head(5),
        y=df["Humidity"].head(5),
        name="Humidity"
    )
    traces.append(bar_2)
    layout = go.Layout(
        barmode="group", xaxis_tickangle=-45, title_text="City's Temperature and Humidity",
        title_font=dict(family="Verdana", size=12, color="black")
    )

    return {"data": traces, "layout": layout}


@app.callback(
    Output("datatable-paging", "data"),
    [Input("datatable-paging", "page_current"),
     Input("datatable-paging", "page_size"),
     Input("interval-component", "n_intervals")]
)
def update_table(page_current, page_size, n):
    global df
    print("Before calling api call in update_table")
    api_endpoint = "http://localhost:8090/wm/v1"  # Fix the typo "localhist" to "localhost"
    api_response = requests.get(api_endpoint)
    record_list = api_response.json()
    df = pd.DataFrame(record_list, columns=["CityName", "Temperature", "Humidity", "CreationTime", "CreationDate"])
    df["index"] = range(1, len(df) + 1)
    print("After Calling api call in update_table")
    print(df.head(10))

    return df.iloc[page_current * page_size:(page_current + 1) * page_size].to_dict('records')


if __name__ == "__main__":
    print("Starting real-time dashboard for weather monitoring app...")
    app.run_server(port=8191, debug=True)