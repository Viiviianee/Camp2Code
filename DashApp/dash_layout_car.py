from dash import html, dcc
import dash_bootstrap_components as dbc

param_speed = html.Div(
    [
        dbc.Label("speed *", html_for="param-speed"),
        dcc.Slider(min=0,max=100, step=5, value=0, id="param-speed")
    ],
    className="mb-3",
)

param_steering_angle = html.Div(
    [
        dbc.Label("steering angle", html_for="param-angle"),
        dcc.Slider(min=45,max=135, step=5, value=90, id="param-angle")
    ],
    className="mb-3",
)

param_time_forward = html.Div(
    [
        dbc.Label("time (forward)", html_for="param-time-forward"),
        dcc.Slider(min=1,max=10, step=1, value=3, id="param-time-forward")
    ],
    className="mb-3",
)

param_time_backward = html.Div(
    [
        dbc.Label("time (backward)", html_for="param-time-backward"),
        dcc.Slider(min=1,max=10, step=1, value=3, id="param-time-backward")
    ],
    className="mb-3",
)

param_time_stop = html.Div(
    [
        dbc.Label("time (stop)", html_for="param-time-stop"),
        dcc.Slider(min=1,max=10, step=1, value=1, id="param-time-stop")
    ],
    className="mb-3",
)

param_min_distance = html.Div(
    [
        dbc.Label("distance (min)", html_for="param-distance"),
        dcc.Slider(min=20, max=60, step=5, id="param-distance")
    ],
    className="mb-3",
)

param_threshold = html.Div(
    [
        dbc.Label("exploring threshold", html_for="param-threshold"),
        dcc.Slider(min=1, max=15, step=1, value=5, id="param-threshold")
    ],
    className="mb-3",
)

param_time_straight = html.Div(
    [
        dbc.Label("driving time (straight)", html_for="param-time-straight"),
        dcc.Slider(min=1, max=10, step=1, value=1, id="param-time-straight")
    ],
    className="mb-3",
)

param_time_curve = html.Div(
    [
        dbc.Label("driving time (curve)", html_for="param-time-curve"),
        dcc.Slider(min=5, max=15, step=1, value=8, id="param-time-curve")
    ],
    className="mb-3",
)



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
