from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
from pathlib import Path
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_layout_components as layout_components
import dash_layout_dashboard as layout_dashboard
import dash_layout_car as layout_car

navbar_tab_names= ["Dashboard", "Car"]
navbar_ids= ["nav-dashboard", "nav-car"]
navbar_logo= "/assets/car.svg"

dropdown_dict = {
    "speed": "Speed",
    "steering_angle": "Steering Angle",
    "distance_ahead": "Distance to object",
    "ir_val": "Line detection",
}

# Logdaten einlesen 
def read_log_data():
    log_path = Path(__file__).resolve().parent.parent.joinpath("Car", "log.csv")
    df = pd.read_csv(log_path)
    return df

app = Dash(
         __name__, external_stylesheets=[
             dbc.themes.BOOTSTRAP, 
             "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            ],
            suppress_callback_exceptions=True 
    )

# App Layout
app.layout = html.Div(
    dbc.Stack(
        [
         layout_components.create_navbar(navbar_logo, navbar_tab_names, navbar_ids),
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content', className="main-container"),
            dcc.Store(id='log-data')  #Unsichtbarer Daten-Storage
        ]
    )
)

#Callback zur Aktualisierung der Log-Daten
@app.callback(
    [Output('log-data', 'data'),
     Output("card-speed-min-value", "figure"),
     Output("card-speed-max-value", "figure"),
     Output("card-speed-mean-value", "figure"),
     Output("card-driving-distance-value", "children"),
     Output("card-driving-time-value", "children"),
     Output("my-dropdown","options" )],
    [Input("load-log-button", "n_clicks")]
)
def update_log_data(n_clicks):
    if n_clicks > 0:
        log_data_df = read_log_data()

        # Dropdown options from log file
        options_list = list(log_data_df.drop('direction', axis=1))
        dd_options = []
        for col in options_list[1:]:
            dd_options.append(dropdown_dict.get(col))

        speeds_greater_than_zero = log_data_df['speed'][log_data_df['speed'] > 0]
        if not speeds_greater_than_zero.empty:
            speed_min_log = round(speeds_greater_than_zero.min(), 1)
        else:
            speed_min_log = 0.0

        speed_max_log = round(log_data_df['speed'].max(), 1)
        speed_mean_log = round(log_data_df['speed'].mean(), 1)
        driving_distance_log = round((log_data_df['speed'] * log_data_df['time']).sum(), 1)
        driving_time_log = round(log_data_df.iloc[-1]['time'] - log_data_df.iloc[0]['time'], 1)

        return [log_data_df.to_dict(),
             layout_components.create_gauge(speed_min_log, "e9c46b"),
             layout_components.create_gauge(speed_max_log, "e66f51"), 
             layout_components.create_gauge(speed_mean_log, "f3a261"), 
                html.H5(driving_distance_log),
                html.H5(driving_time_log),
                [{"label": dropdown_dict.get(col), "value": col} for col in options_list[1:]]
            ]
    
    return [None, layout_components.create_gauge(0.0, "e9c46b"), layout_components.create_gauge(0.0, "e66f51"), layout_components.create_gauge(0.0, "f3a261"), "0.0", "0.0", []]

#Callback zur Aktualisierung des Dropdowns und des Graph
@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='my-dropdown', component_property='value'),
    State('log-data', 'data')
)
def update_graph(value, data, dropdown_dict=dropdown_dict):
    print(value)
    if value:
        df = pd.DataFrame.from_dict(data)
        df['speed'] = df['speed'] * df['direction']
        
        figure = px.line(
            df,
            x='time',
            y=value,
            labels={"time": "time [s]", value: dropdown_dict.get(value)}
        )
        # if value == "ir_val":
        #     figure.update_layout(
        #         yaxis=dict(
        #             tickvals=[],
        #             ticktext=ticktext,
        #             title=dropdown_dict.get(value, value)  # Dynamische Titel für die Y-Achse
        #         )
        #     )
    else:
        figure = px.line()
    return figure

# Callback für das Laden des richtigen Inhalts basierend auf der URL
@app.callback(
    [Output('page-content', 'children'),
     Output('nav-dashboard', 'active'), 
     Output('nav-car', 'active')],
    [Input('url', 'pathname')]  
)
def display_page(pathname):
    if pathname is None or pathname == '/' or pathname =='/Dashboard':
        return [layout_dashboard.content, pathname == '/' or pathname =='/Dashboard', pathname == '/Car']
    elif pathname == '/Car':
        return [layout_car.content, pathname == '/' or pathname =='/Dashboard', pathname == '/Car']
  
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8051)
