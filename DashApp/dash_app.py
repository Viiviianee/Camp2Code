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
import dash_layout_cam as layout_cam
import sys
from flask import Flask, Response, request
import numpy as np
import cv2
import threading

# Add project path for additional modules
project_path = Path(__file__).resolve().parent.parent / 'Car'
sys.path.append(str(project_path))
from SensorCar.sensor_car_alternative_algo import SensorCar
from CamCar import CamCar
from OpenCVCar import Opencvcar

# Configuration for navigation and UI elements
NAVBAR_TAB_NAMES = ["Dashboard", "Car", "Cam"]
NAVBAR_IDS = ["nav-dashboard", "nav-car", "nav-cam"]
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
server = Flask(__name__)
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    suppress_callback_exceptions=False,
    server=server
)

car = Opencvcar()

@server.route("/Cam/video_feed1")
def video_feed1():
    """Will return the video feed from the camera

    Returns:
        Response: Response object with the video feed
    """
    return Response(
        car.helper_1(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

# @server.route("/Cam/video_feed2")
# def video_feed2():
#     """Will return the video feed from the camera

#     Returns:
#         Response: Response object with the video feed
#     """
#     return Response(
#         car.helper_2(),
#         mimetype="multipart/x-mixed-replace; boundary=frame",
#     )

# @server.route("/Cam/video_feed3")
# def video_feed3():
#     """Will return the video feed from the camera

#     Returns:
#         Response: Response object with the video feed
#     """
#     return Response(
#         car.helper_3(),
#         mimetype="multipart/x-mixed-replace; boundary=frame",
#     )

# @server.route("/Cam/video_feed4")
# def video_feed4():
#     """Will return the video feed from the camera

#     Returns:
#         Response: Response object with the video feed
#     """
#     return Response(
#         car.helper_4(),
#         mimetype="multipart/x-mixed-replace; boundary=frame",
#     )


# Layout configuration
app.layout = html.Div(
    [
    dbc.Stack([
        layout_components.create_navbar(NAVBAR_LOGO, NAVBAR_TAB_NAMES, NAVBAR_IDS),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', className="main-container"),
        dcc.Store(id='log-data'),
        dcc.Store(id='temp-data'),
        html.Div(id="dummy-output1", style={"display": "none"}),
        html.Div(id="dummy-output2", style={"display": "none"})
        
    ])
    ]
)

# Callback für das Laden des richtigen Inhalts basierend auf der URL
@app.callback(
    [Output('page-content', 'children'),
     Output('nav-dashboard', 'active'),
     Output('nav-car', 'active'),
     Output('nav-cam', 'active')],
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname is None or pathname == '/' or pathname =='/Dashboard':
        return [layout_dashboard.content, pathname == '/' or pathname =='/Dashboard', pathname == '/Car', pathname == '/Cam']
    elif pathname == '/Car':
        return [layout_car.content, pathname == '/' or pathname =='/Dashboard', pathname == '/Car', pathname == '/Cam']
    elif pathname == '/Cam':
        return [layout_cam.content, pathname == '/' or pathname =='/Dashboard', pathname == '/Car', pathname == '/Cam']

#Fahrmodus OpenCV oder Neuronales Netz
@app.callback(
    Output("dummy-output1", "children"),
    [Input("start-btn-cam-car", "n_clicks"),
     Input('my-select-cam-car', 'value')
    ],
    prevent_initial_call=True
)
def start_Fahrmodus(n_clicks, selected_option):
    if n_clicks and n_clicks > 0:
        if selected_option == '1':
            car.fahrmodus_cam()
        elif selected_option == '2':
            pass
    return no_update

@app.callback(
    Output("dummy-output2", "children"),
    [Input("stop-btn-cam-car", "n_clicks")],
    prevent_initial_call=True
)
def stop_Fahrmodus(n_clicks):
    if n_clicks and n_clicks > 0:
        car.stop()
    return no_update


@app.callback(
    Output("Wert_Slider_1", "children"),
    Output("Wert_Slider_2", "children"),
    Output("Wert_Slider_3", "children"),
    Output("Wert_Slider_4", "children"),
    Output("Wert_Slider_5", "children"),
    Output("Wert_Slider_6", "children"),
    Output("Wert_Slider_7", "children"),
    Output("Wert_Slider_8", "children"),
    Input("range-slider-1", "value"),
    Input("range-slider-2", "value"),
    Input("range-slider-3", "value"),
    Input("range-slider-4", "value"),
    Input("range-slider-5", "value"),
    Input("range-slider-6", "value"),
    Input("range-slider-7", "value"),
    Input("range-slider-8", "value"),
)
def update_values(range_slider_1, 
                  range_slider_2, 
                  range_slider_3, 
                  range_slider_4,
                  range_slider_5,
                  range_slider_6,
                  range_slider_7,
                  range_slider_8,):  # Parameter definiert über Input von app.callback
    h_low, h_high = range_slider_1
    s_low, s_high = range_slider_2
    v_low, v_high = range_slider_3
    threshold = range_slider_4
    minLineLength_slider_val = range_slider_5
    maxLineGap_val = range_slider_6
    canny_min_val = range_slider_7
    canny_max_val = range_slider_8
    car.lower_h = h_low
    car.upper_h = h_high
    car.lower_s = s_low
    car.upper_s = s_high
    car.lower_v = v_low
    car.upper_v = v_high
    car.threshold = threshold
    car.minLineLength_slider_val = minLineLength_slider_val
    car.maxLineGap_val = maxLineGap_val
    car.canny_min_val = canny_min_val
    car.canny_max_val = canny_max_val
    print(f"Werte von processor Klasse Parameter h: {car.lower_h}, {car.upper_h}")
    print(f"Werte von processor Klasse Parameter s: {car.lower_s}, {car.upper_s}")
    print(f"Werte von processor Klasse Parameter v: {car.lower_v}, {car.upper_v}")
    print(f"Werte von processor Klasse Parameter threshold: {car.threshold}")
    print(f"Werte von processor Klasse Parameter minLineLength: {car.minLineLength_slider_val}")
    print(f"Werte von processor Klasse Parameter maxLineGap: {car.maxLineGap_val}")
    print(f"Werte von processor Klasse Parameter canny_min: {car.canny_min_val}")
    print(f"Werte von processor Klasse Parameter canny_max: {car.canny_max_val}")
    print(40*"**")
    return f"Slider für Parameter h: {h_low} und {h_high}.",\
           f"Slider für Parameter s: {s_low} und {s_high}.",\
           f"Slider für Parameter v: {v_low} und {v_high}.",\
           f"Slider für Parameter threshold: {threshold}.",\
           f"Slider für Parameter minLineLength: {minLineLength_slider_val}.",\
           f"Slider für Parameter maxLineGap: {maxLineGap_val}.",\
           f"Slider für Parameter canny_min: {canny_min_val}.",\
           f"Slider für Parameter canny_max: {canny_max_val}.",\

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
                labels={"time": "time [s]", value: DROPDOWN_DICT.get(value)}
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
    app.run_server(host="0.0.0.0", port=8050, debug=False,  use_reloader=False)  # Debug ist false wegen Kamera
    #app.run_server(debug=True, host="0.0.0.0", port=8054, threaded=True, use_reloader=False)
    #threading.Thread(target=app.run, kwargs={'debug': False, 'port': 8052, 'host':"0.0.0.0", 'threaded': True}).start()