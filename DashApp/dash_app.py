"""
Main application for a car sensor-based dashboard using Dash.
Provides navigation, data visualization, and control interfaces.
"""

from dash import Dash, html, dcc, Input, Output, State, no_update, callback_context
import pandas as pd
from pathlib import Path
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_layout_components as layout_components
import dash_layout_dashboard as layout_dashboard
import dash_layout_car as layout_car
import sys

# Add project path for additional modules
project_path = Path(__file__).resolve().parent.parent / 'Car'
sys.path.append(str(project_path))
from SensorCar.sensor_car_alternative_algo import SensorCar

# Configuration for navigation and UI elements
NAVBAR_TAB_NAMES = ["Dashboard", "Car"]
NAVBAR_IDS = ["nav-dashboard", "nav-car"]
NAVBAR_LOGO = "/assets/car.svg"

DROPDOWN_DICT = {
    "speed": "Speed",
    "steering_angle": "Steering Angle",
    "distance_ahead": "Distance to object",
    "ir_val": "Line detection",
}

def read_log_data():
    """Reads log data from the car's log file."""
    log_path = project_path / "log.csv"
    return pd.read_csv(log_path)

# Initialize Dash app with Bootstrap and external stylesheets
app = Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP, 
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)

# Layout configuration
app.layout = html.Div(
    dbc.Stack([
        layout_components.create_navbar(NAVBAR_LOGO, NAVBAR_TAB_NAMES, NAVBAR_IDS),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', className="main-container"),
        dcc.Store(id='log-data'),
        dcc.Store(id='temp-data')
    ])
)

@app.callback(
    [Output('log-data', 'data'),
     Output("card-speed-min-value", "figure"),
     Output("card-speed-max-value", "figure"),
     Output("card-speed-mean-value", "figure"),
     Output("card-driving-distance-value", "children"),
     Output("card-driving-time-value", "children"),
     Output("my-dropdown", "options")],
    [Input("load-log-button", "n_clicks")]
)
def update_log_data(n_clicks):
    """Updates log data and associated UI elements when the button is clicked."""
    if n_clicks > 0:
        log_data_df = read_log_data()
        options_list = list(log_data_df.drop('direction', axis=1))
        dropdown_options = [{"label": DROPDOWN_DICT.get(col, col), "value": col} for col in options_list[1:]]
        
        speeds_greater_than_zero = log_data_df['speed'][log_data_df['speed'] > 0]
        speed_min_log = round(speeds_greater_than_zero.min(), 1) if not speeds_greater_than_zero.empty else 0.0
        speed_max_log = round(log_data_df['speed'].max(), 1)
        speed_mean_log = round(log_data_df['speed'].mean(), 1)
        driving_time_log = round(log_data_df.iloc[-1]['time'] - log_data_df.iloc[0]['time'], 1)
        driving_distance_log = round((speed_mean_log / 2) * driving_time_log, 1)

        return [
            log_data_df.to_dict(),
            layout_components.create_gauge(speed_min_log, "e9c46b"),
            layout_components.create_gauge(speed_max_log, "e66f51"),
            layout_components.create_gauge(speed_mean_log, "f3a261"),
            html.H5(f"{driving_distance_log} cm"),
            html.H5(f"{driving_time_log} s"),
            dropdown_options
        ]
    return [None, *[layout_components.create_gauge(0.0, color) for color in ["e9c46b", "e66f51", "f3a261"]], "0 cm", "0 s", []]

#Callback zur Aktualisierung des Dropdowns und des Graph
@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='my-dropdown', component_property='value'),
    State('log-data', 'data')
)
def update_graph(value, data):
    if value:
        df = pd.DataFrame.from_dict(data)
        df['speed'] = df['speed'] * df['direction']
        if value == "ir_val":
            figure = px.scatter(
                df,
                x='time',
                y=value,
                labels={"time": "time [s]", value: dropdown_dict.get(value)}
            )
            figure.update_traces(marker=dict(size=10))
            figure.update_layout(
                yaxis=dict(
                    tickvals = list(range(32)),  # 0 bis 31 für alle möglichen Binärkombinationen
                    ticktext = [
                        "[0, 0, 0, 0, 0]",
                        "[0, 0, 0, 0, 1]",
                        "[0, 0, 0, 1, 0]",
                        "[0, 0, 0, 1, 1]",
                        "[0, 0, 1, 0, 0]",
                        "[0, 0, 1, 0, 1]",
                        "[0, 0, 1, 1, 0]",
                        "[0, 0, 1, 1, 1]",
                        "[0, 1, 0, 0, 0]",
                        "[0, 1, 0, 0, 1]",
                        "[0, 1, 0, 1, 0]",
                        "[0, 1, 0, 1, 1]",
                        "[0, 1, 1, 0, 0]",
                        "[0, 1, 1, 0, 1]",
                        "[0, 1, 1, 1, 0]",
                        "[0, 1, 1, 1, 1]",
                        "[1, 0, 0, 0, 0]",
                        "[1, 0, 0, 0, 1]",
                        "[1, 0, 0, 1, 0]",
                        "[1, 0, 0, 1, 1]",
                        "[1, 0, 1, 0, 0]",
                        "[1, 0, 1, 0, 1]",
                        "[1, 0, 1, 1, 0]",
                        "[1, 0, 1, 1, 1]",
                        "[1, 1, 0, 0, 0]",
                        "[1, 1, 0, 0, 1]",
                        "[1, 1, 0, 1, 0]",
                        "[1, 1, 0, 1, 1]",
                        "[1, 1, 1, 0, 0]",
                        "[1, 1, 1, 0, 1]",
                        "[1, 1, 1, 1, 0]",
                        "[1, 1, 1, 1, 1]"
                    ]    
                )
            )
        else:
            figure = px.line(
                df,
                x='time',
                y=value,
                labels={"time": "time [s]", value: DROPDOWN_DICT.get(value)}
            )
        
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

@app.callback(
    [Output("my-traffic-light", "src", allow_duplicate=True),Output('param-speed', 'disabled'),Output('param-angle', 'disabled'),Output('param-time-forward', 'disabled'),Output('param-time-backward', 'disabled'),Output('param-time-stop', 'disabled'),Output('param-distance', 'disabled'),Output('param-threshold', 'disabled'), Output('param-time-straight', 'disabled'),Output('param-time-curve', 'disabled')],
    [Input('my-select', 'value'), Input("start-btn", "n_clicks")],
    prevent_initial_call=True
)
def update_form(selected_option, n_clicks):
    src_yellow= "/assets/traffic-light-yellow.svg"
    src_red= "/assets/traffic-light-red.svg"
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'my-select':
            if selected_option == '1':
                return [src_red, False, True, False, False, False, True, True, True, True]
            elif selected_option == '2':
                return [src_red, False, False, True, True, True, True, True, False, False]
            elif selected_option == '3':
                return [src_red, False, False, True, True, True, False, True, True, True]
            elif selected_option == '4':
                return [src_red, False, True, True, True, True, True, False, True, True ]
            elif selected_option == '5' or selected_option == '6' or selected_option == '7':
                return [src_red, False, True, True, True, True, True, True, True, True]
            else:
                return [src_red, True, True, True, True, True, True, True, True, True]
            
        elif trigger_id == 'start-btn':
            if n_clicks > 0:
                return [src_yellow,True, True, True, True, True, True, True, True, True]
        
    return no_update
    
#Fahrmodus 1
@app.callback(
    [Output('my-traffic-light', 'src', allow_duplicate=True), Output('start-btn', 'disabled'), Output('my-select', 'disabled')],
    [Input("start-btn", "n_clicks"), Input('param-speed', 'value')],
    prevent_initial_call='initial_duplicate'
)
def update_traffic_light_and_start_btn(n_clicks,value):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'start-btn'and n_clicks > 0:
            return ["/assets/traffic-light-yellow.svg", True, True]
        elif trigger_id == 'param-speed':
            return ["/assets/traffic-light-red.svg", value == 0, False]
    return no_update

#Fahrmodus 
@app.callback(
    [Output('my-traffic-light', 'src', allow_duplicate=True), Output("start-btn", "disabled", allow_duplicate=True), Output('my-select', 'disabled', allow_duplicate=True)],
    [Input("start-btn", "n_clicks")],
    [State("param-speed", "value"), State("param-time-forward", "value"), State("param-time-backward", "value"), State("param-time-stop", "value"), 
     State("param-distance", "value"), State("param-angle", "value"), State("param-threshold", "value"), State("param-time-straight", "value"), State("param-time-curve", "value"), State("my-select", "value")],
    prevent_initial_call='initial_duplicate'
)
def run_fahrmodus(n_clicks, speed, t_forward, t_backward, t_stop, distance, angle, 
                  threshold, time_straight, time_curve, selected_option):
    if n_clicks and n_clicks > 0:
        car = SensorCar()
        if selected_option == '1':
            car.fahrmodus1(speed, t_forward, t_backward, t_stop)
        elif selected_option == '2':
            lst= [
                {"speed" : speed, "steering_angle" : 90, "time" : time_straight, "stop" : 1},
                {"speed" : speed, "steering_angle" : angle, "time" : time_curve, "stop" : 1},
                {"speed" : -speed, "steering_angle" : angle, "time" : time_curve, "stop" : 1},
                {"speed" : -speed, "steering_angle" : 90, "time" : time_straight, "stop" : 1},
                {"speed" : speed, "steering_angle" : 90, "time" : time_straight, "stop" : 1},
                {"speed" : speed, "steering_angle" : 180-angle, "time" : time_curve, "stop" : 1},
                {"speed" : -speed, "steering_angle" : 180-angle, "time" : time_curve, "stop" : 1},
                {"speed" : -speed, "steering_angle" : 90, "time" : time_straight, "stop" : 1},   
            ]
            car.fahrmodus1_2(lst=lst)
        elif selected_option == '3':
            car.fahrmodus3(speed, distance, angle)
        elif selected_option == '4':
            car.fahrmodus4(speed, threshold)
        elif selected_option == '5':
            car.fahrmodus5(speed)
        elif selected_option == '6':
            car.fahrmodus6(speed)
        elif selected_option == '7':
            car.fahrmodus7(speed)
        
        return ["/assets/traffic-light-green.svg", False, False]
    return no_update


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8052)
