from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_layout_components as c

# Define individual parameter components using pre-built function
param_speed = c.create_param_div("speed *", min=0, max=100, step=5, value=0, id="param-speed", disabled=True)
param_steering_angle = c.create_param_div("steering angle", min=45, max=135, step=5, value=90, id="param-angle", disabled=True)
param_time_forward = c.create_param_div("time (forward)", min=1, max=10, step=1, value=3, id="param-time-forward", disabled=True)
param_time_backward = c.create_param_div("time (backward)", min=1, max=10, step=1, value=3, id="param-time-backward", disabled=True)
param_time_stop = c.create_param_div("time (stop)", min=1, max=10, step=1, value=1, id="param-time-stop", disabled=True)
param_min_distance = c.create_param_div("distance (min)", min=20, max=60, step=5, value=20, id="param-distance", disabled=True)
param_threshold = c.create_param_div("exploring threshold", min=1, max=15, step=1, value=5, id="param-threshold", disabled=True)
param_time_straight = c.create_param_div("driving time (straight)", min=1, max=10, step=1, value=1, id="param-time-straight", disabled=True)
param_time_curve = c.create_param_div("driving time (curve)", min=5, max=15, step=1, value=8, id="param-time-curve", disabled=True)

# Form layout for parameter input
form_fahrmodus = dbc.Stack(
    [
        dbc.Row(dbc.Col(param_speed)),
        dbc.Row(
            [
                dbc.Col(param_time_forward),
                dbc.Col(param_time_backward),
                dbc.Col(param_time_stop)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(param_time_straight),
                dbc.Col(param_time_curve)
            ]
        ),
        dbc.Row(dbc.Col(param_steering_angle)),
        dbc.Row(
            [
                dbc.Col(param_min_distance),
                dbc.Col(param_threshold)
            ]
        )
    ],
    gap=4
)

# Main content layout
content = dbc.Row(
    [
        dbc.Col(
            dbc.Stack(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Select(
                                    placeholder="Fahrmodus",
                                    id="my-select",
                                    options=[
                                        {"label": "Fahrmodus 1", "value": "1"},
                                        {"label": "Fahrmodus 2", "value": "2"},
                                        {"label": "Fahrmodus 3", "value": "3"},
                                        {"label": "Fahrmodus 4", "value": "4"},
                                        {"label": "Fahrmodus 5", "value": "5"},
                                        {"label": "Fahrmodus 6", "value": "6"},
                                        {"label": "Fahrmodus 7", "value": "7"},
                                    ],
                                ),
                                className="col-10"
                            ),
                            dbc.Col(
                                dbc.Button("Start", className="custom-btn w-100", id="start-btn", disabled=True, n_clicks=0),
                                className="col-2"
                            ),
                        ],
                        className="g-3"
                    ),
                    html.Div(form_fahrmodus, id="form-param-fahrmodus")   
                ],
                gap=5
            ),
            className="col-9"
        ),
        dbc.Col(
            html.Img(src="/assets/traffic-light-red.svg", height="300px", className="navbar-logo", id="my-traffic-light"),
            className="col-3"
        )
    ],
    className="row-cols-2"
)